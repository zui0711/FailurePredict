import os
import numpy as np
import time

import tensorflow as tf

from configs.data_config import *
from lib.data_utils import *
from lib.seq2seq_score import get_score
from models.seq2seq import create_model

def predict():
    def _get_test_dataset(encoder_size):
        with open(TEST_DATASET_PATH) as test_fh:
            test_sentences = []
            for line in test_fh.readlines():
                sen = [int(x) for x in line.strip().split()[:encoder_size]]
                if sen:
                    test_sentences.append((sen, []))
        return test_sentences

    bucket_id = 0

    max_len = BUCKETS[bucket_id][0]

    vocab_path = os.path.join(FLAGS.data_dir, "vocab%d.txt" % FLAGS.vocab_size)
    vocab, rev_vocab = initialize_vocabulary(vocab_path)

    test_dataset = _get_test_dataset(max_len)
    test_len = len(test_dataset)
    batch_size = FLAGS.predict_batch_size
    batch_num = test_len / batch_size + (0 if test_len % batch_size == 0 else 1)

    file_r = pjoin(SAVE_DATA_DIR, "test/decode.txt")

    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    with tf.Session(config=config) as sess:
        model = create_model(sess, forward_only=True)
        for predict_step in range(5000, 35000, 5000):
            predict_path = pjoin(FLAGS.model_dir, "model.ckpt-%d" % predict_step)
            print("Reading model parameters from %s" % predict_path)
            model.saver.restore(sess, predict_path)
            model.batch_size = FLAGS.predict_batch_size

            results_filename = 'results(%d, %d).%d' % (max_len, max_len, model.global_step.eval())
            results_filename_ids = "results(%d, %d).ids%d.%d" % (max_len, max_len, FLAGS.vocab_size, model.global_step.eval())

            results_path = os.path.join(FLAGS.results_dir, results_filename)
            results_path_ids = os.path.join(FLAGS.results_dir, results_filename_ids)

            with open(results_path, 'w') as results_f, open(results_path_ids, 'w') as results_f_ids:
                start_time = time.time()
                for num in xrange(batch_num - 1):
                    this_batch = test_dataset[batch_size*num: batch_size*(num+1)]
                    encoder_inputs, decoder_inputs, target_weights = model.get_batch(this_batch, bucket_id, "predict")
                    _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)

                    for b in xrange(batch_size):
                        outputs = []
                        for en in xrange(max_len):
                            selected_token_id = int(np.argmax(output_logits[en][b]))

                            if selected_token_id == EOS_ID:
                                break
                            else:
                                outputs.append(selected_token_id)

                        output_sentence = ' '.join([rev_vocab[output] for output in outputs])
                        output_sentence_ids = ' '.join([str(output) for output in outputs])

                        # if output_sentence == "":
                        #     print(num, b, output)

                        results_f.write(output_sentence + '\n')
                        results_f_ids.write(output_sentence_ids + "\n")
                    # print("batch %d finish..."%num)
                t = time.time() - start_time
                print("predict: total time = %0.2f, per time = %0.2f" % (t, t / float(batch_num - 1)))

            # print("Predict finish...")

            print file_r, results_path
            get_score(file_r, results_path)
