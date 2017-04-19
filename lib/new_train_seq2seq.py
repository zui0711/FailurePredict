import sys
import os
import math
import time

import numpy as np

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf

from models.seq2seq import create_model
from configs.data_config import FLAGS, BUCKETS
from lib.data_utils import *
from lib import data_utils


def train():
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    print("Preparing dialog data in %s" % FLAGS.data_dir)
    train_data, dev_data, _ = data_utils.prepare_dialog_data(FLAGS.data_dir, FLAGS.vocab_size)

    with tf.Session() as sess:

        # Create model.
        print("Creating %d layers of %d units." % (FLAGS.num_layers, FLAGS.hidden_size))
        model = create_model(sess, forward_only=False)

        # Read data into buckets and compute their sizes.
        print ("Reading development and training data (limit: %d)." % FLAGS.max_train_data_size)
        dev_set = read_data(dev_data)
        train_set = read_data(train_data, FLAGS.max_train_data_size)
        train_bucket_sizes = [len(train_set[b]) for b in xrange(len(BUCKETS))]
        train_total_size = float(sum(train_bucket_sizes))

        # A bucket scale is a list of increasing numbers from 0 to 1 that we'll use
        # to select a bucket. Length of [scale[i], scale[i+1]] is proportional to
        # the size if i-th training bucket, as used later.
        train_buckets_scale = [sum(train_bucket_sizes[:i + 1]) / train_total_size for i in xrange(len(train_bucket_sizes))]


        print("Reading predict data...")
        encoder_size = 360
        test_dataset = []
        with open(TEST_DATASET_PATH) as test_fh:
            for line in test_fh.readlines():
                sen = [int(x) for x in line.strip().split()[:encoder_size]]
                if sen:
                    test_dataset.append((sen, []))

        print("Reading vocab...")
        vocab_path = pjoin(FLAGS.data_dir, "vocab%d.txt" % FLAGS.vocab_size)
        vocab, rev_vocab = initialize_vocabulary(vocab_path)


        # This is the training loop.
        step_time, total_time, loss = 0.0, 0.0, 0.0
        current_step = 0
        previous_losses = []

        print("start train...")
        while (True):
            # Choose a bucket according to data distribution. We pick a random number
            # in [0, 1] and use the corresponding interval in train_buckets_scale.
            random_number_01 = np.random.random_sample()
            bucket_id = min([i for i in xrange(len(train_buckets_scale)) if train_buckets_scale[i] > random_number_01])

            # Get a batch and make a step.
            start_time = time.time()
            encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                train_set, bucket_id, "train")

            _, step_loss, _ = model.step(sess, encoder_inputs, decoder_inputs,
                                       target_weights, bucket_id, forward_only=False)

            step_time += (time.time() - start_time) / FLAGS.steps_per_checkpoint
            loss += step_loss / FLAGS.steps_per_checkpoint
            current_step += 1

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if model.global_step % FLAGS.steps_per_checkpoint == 0:
                # Print statistics for the previous epoch.
                perplexity = math.exp(loss) if loss < 300 else float('inf')
                total_time = step_time * FLAGS.steps_per_checkpoint
                print ("global step %d learning rate %.4f step-time %.2f total_time %.4f perplexity %.4f, loss %0.7f" %
                       (model.global_step.eval(), model.learning_rate.eval(), step_time, total_time, perplexity, loss))

                # Decrease learning rate if no improvement was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(model.learning_rate_decay_op)

                previous_losses.append(loss)

                # Save checkpoint and zero timer and loss.
                checkpoint_path = os.path.join(FLAGS.model_dir, "model.ckpt")
                model.saver.save(sess, checkpoint_path, global_step=model.global_step)
                step_time, loss = 0.0, 0.0

                # Run evals on development set and print their perplexity.
                for bucket_id in xrange(len(BUCKETS)):
                    encoder_inputs, decoder_inputs, target_weights = model.get_batch(dev_set, bucket_id, "train")
                    _, eval_loss, _ = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)

                    eval_ppx = math.exp(eval_loss) if eval_loss < 300 else float('inf')
                    print("  eval: bucket %d perplexity %.4f, loss %0.7f" % (bucket_id, eval_ppx, eval_loss))

                sys.stdout.flush()


                if model.global_step % FLAGS.steps_per_predictpoint == 0:

                    results_filename = 'results(%d, %d).txt_%d' % (BUCKETS[0][0], BUCKETS[0][0], model.global_step)
                    # results_filename_ids = '.'.join(['results' + str(BUCKETS[0]), "ids" + str(FLAGS.vocab_size), "txt"])
                    results_filename_ids = "results(%d, %d).ids%d.txt_%d" % \
                                           (LSTM_max_len, LSTM_max_len, FLAGS.vocab_size, model.global_step)

                    results_path = os.path.join(FLAGS.results_dir, results_filename)
                    results_path_ids = os.path.join(FLAGS.results_dir, results_filename_ids)

                    with open(results_path, 'w') as results_f, open(results_path_ids, 'w') as results_f_ids:

                        # encoder_size, decoder_size = model.buckets[0]

                        batch_size = FLAGS.predict_batch_size
                        test_len = len(test_dataset)
                        batch_num = test_len / batch_size + (0 if test_len % batch_size == 0 else 1)

                        for num in xrange(batch_num - 1):
                            this_batch = test_dataset[batch_size * num: batch_size * (num + 1)]
                            encoder_inputs, decoder_inputs, target_weights = model.get_batch(this_batch, bucket_id, "predict")
                            _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id,
                                                             True)

                            for b in xrange(batch_size):
                                outputs = []
                                for en in xrange(encoder_size):
                                    selected_token_id = int(np.argmax(output_logits[en][b]))

                                    if selected_token_id == EOS_ID:
                                        break
                                    else:
                                        outputs.append(selected_token_id)
                                output_sentence = ' '.join([rev_vocab[output] for output in outputs])
                                output_sentence_ids = ' '.join([str(output) for output in outputs])

                                results_f.write(output_sentence + '\n')
                                results_f_ids.write(output_sentence_ids + "\n")

