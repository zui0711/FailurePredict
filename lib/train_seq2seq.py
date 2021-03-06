import sys
import os
import math
import time

import numpy as np

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf

from models.seq2seq import create_model
from configs.data_config import FLAGS, BUCKETS, pjoin
from lib.data_utils import read_data
from lib import data_utils


def train():
    print("Preparing dialog data in %s" % FLAGS.data_dir)
    train_data, dev_data, _ = data_utils.prepare_dialog_data(FLAGS.data_dir, FLAGS.vocab_size)

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:

        record_file_name = "seq2seq_loss"
        record_file = open(pjoin(FLAGS.results_dir, record_file_name), mode="ab", buffering=0)

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
        train_buckets_scale = [sum(train_bucket_sizes[:i + 1]) / train_total_size
                               for i in xrange(len(train_bucket_sizes))]

        # This is the training loop.
        step_time, total_time, loss = 0.0, 0.0, 0.0
        previous_losses = []

        print("start train...")
        while (True):
            # Choose a bucket according to data distribution. We pick a random number
            # in [0, 1] and use the corresponding interval in train_buckets_scale.
            random_number_01 = np.random.random_sample()
            bucket_id = min([i for i in xrange(len(train_buckets_scale))
                           if train_buckets_scale[i] > random_number_01])

            # Get a batch and make a step.
            start_time = time.time()
            encoder_inputs, decoder_inputs, target_weights = model.get_batch(
                train_set, bucket_id, "train")

            _, step_loss, _ = model.step(sess, encoder_inputs, decoder_inputs,
                                       target_weights, bucket_id, forward_only=False)

            step_time += (time.time() - start_time) / FLAGS.steps_per_checkpoint
            loss += step_loss / FLAGS.steps_per_checkpoint

            # Once in a while, we save checkpoint, print statistics, and run evals.
            if model.global_step.eval() % FLAGS.steps_per_checkpoint == 0:
                print("\nTraining...")
                if loss > 6:
                    print("inf !!!")
                    sys.exit(0)
                total_time = step_time * FLAGS.steps_per_checkpoint
                print ("global step %d learning rate %.4f step-time %.2f total_time %.4f, loss %0.7f" %
                       (model.global_step.eval(), model.learning_rate.eval(), step_time, total_time, loss))

                # Decrease learning rate if no improvement was seen over last 3 times.
                if len(previous_losses) > 2 and loss > max(previous_losses[-3:]):
                    sess.run(model.learning_rate_decay_op)

                previous_losses.append(loss)

                # Run evals on development set and print their perplexity.
                for bucket_id in xrange(len(BUCKETS)):
                    print("Testing...")

                    encoder_inputs, decoder_inputs, target_weights = model.get_batch(dev_set, bucket_id, "train")
                    _, eval_loss, _ = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)

                    if eval_loss > 6:
                        print("inf !!!")
                        sys.exit(0)

                    print("eval: bucket %d, loss %0.5f" % (bucket_id, eval_loss))

                sys.stdout.flush()
                record_file.write("%d\t%.5f\t%.5f\n" % (model.global_step.eval(), loss, eval_loss))

                # Save checkpoint and zero timer and loss.
                if model.global_step.eval() % FLAGS.steps_per_predictpoint == 0:
                    checkpoint_path = os.path.join(FLAGS.model_dir, "model.ckpt")
                    model.saver.save(sess, checkpoint_path, global_step=model.global_step)
                step_time, loss = 0.0, 0.0
