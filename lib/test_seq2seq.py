import os
import numpy as np

import tensorflow as tf

from configs.data_config import *
from lib.data_utils import *
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
    results_filename = 'results' + str(BUCKETS[bucket_id]) + ".txt"
    results_filename_ids = '.'.join(['results'+str(BUCKETS[bucket_id]), "ids"+str(FLAGS.vocab_size), "txt"])

    results_path = os.path.join(FLAGS.results_dir, results_filename)
    results_path_ids = os.path.join(FLAGS.results_dir, results_filename_ids)
    with tf.Session() as sess, open(results_path, 'w') as results_f, \
            open(results_path_ids, 'w') as results_f_ids:
        batch_size = 128
        model = create_model(sess, forward_only=True)
        model.batch_size = batch_size

        vocab_path = os.path.join(FLAGS.data_dir, "vocab%d.txt" % FLAGS.vocab_size)
        vocab, rev_vocab = initialize_vocabulary(vocab_path)

        encoder_size, decoder_size = model.buckets[bucket_id]
        test_dataset = _get_test_dataset(encoder_size)
        test_len = len(test_dataset)
        batch_num = test_len / batch_size + (0 if test_len%batch_size == 0 else 1)

        for num in xrange(batch_num - 1):
            this_batch = test_dataset[batch_size*num: batch_size*(num+1)]
            encoder_inputs, decoder_inputs, target_weights = model.get_batch(this_batch, bucket_id, "predict")
            _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, True)

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
            print("batch %d finish..."%num)
