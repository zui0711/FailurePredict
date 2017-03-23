import os

import tensorflow as tf

from configs.config import TEST_DATASET_PATH, FLAGS
from lib import data_utils
from models.seq2seq import create_model


def predict():
    def _get_test_dataset():
        with open(TEST_DATASET_PATH) as test_fh:
            test_sentences = []
            for line in test_fh.readlines():
                sen = [int(x) for x in line.strip().split()]
                # test_sentences = [s.strip() for s in test_fh.readlines()]
                #test_sentences = [int(x) for x in test_sentences]
                if sen:
                    test_sentences.append(sen)

        return test_sentences

    results_filename = '_'.join(['results', str(FLAGS.num_layers), str(FLAGS.size), str(FLAGS.vocab_size)])
    results_path = os.path.join(FLAGS.results_dir, results_filename)

    with tf.Session() as sess, open(results_path, 'w') as results_fh:
        # Create model and load parameters.
        batch_size = 1
        model = create_model(sess, forward_only=True)
        model.batch_size = batch_size  # We decode one sentence at a time.

        # Load vocabularies.
        vocab_path = os.path.join(FLAGS.data_dir, "vocab%d.in" % FLAGS.vocab_size)
        vocab, rev_vocab = data_utils.initialize_vocabulary(vocab_path)

        test_dataset = _get_test_dataset()

        #batch_num = len(test_dataset) / batch_size + 1

        for sentence in test_dataset:
        #for num in range(batch_num):
            #sentences = test_dataset[num*batch_size: (num+1)*batch_size]
            # Get token-ids for the input sentence.
            predicted_sentence = get_predicted_sentence(sentence, vocab, rev_vocab, model, sess)
            # print(sentence)
            # print('    ->')
            # print(predicted_sentence)
            # print("\n")

            results_fh.write(predicted_sentence + '\n')


def get_predicted_sentence(input_token_ids, vocab, rev_vocab, model, sess):
    #input_token_ids = data_utils.sentence_to_token_ids(input_sentence, vocab)

    # Which bucket does it belong to?
    # bucket_id = min([b for b in xrange(len(BUCKETS)) if BUCKETS[b][0] > len(input_token_ids)])
    # bucket = [(x, x)]
    bucket_id = 0
    outputs = []

    feed_data = {bucket_id: [(input_token_ids, outputs)]}
    # Get a 1-element batch to feed the sentence to the model.
    encoder_inputs, decoder_inputs, target_weights = model.get_batch(feed_data, bucket_id)

    # Get output logits for the sentence.
    _, _, output_logits = model.step(sess, encoder_inputs, decoder_inputs, target_weights, bucket_id, forward_only=True)

    outputs = []
    # This is a greedy decoder - outputs are just argmaxes of output_logits.
    for logit in output_logits:
        selected_token_id = int(np.argmax(logit, axis=1))

        if selected_token_id == data_utils.EOS_ID:
            break
        else:
            outputs.append(selected_token_id)

    # Forming output sentence on natural language
    output_sentence = ' '.join([rev_vocab[output] for output in outputs])

    return output_sentence
