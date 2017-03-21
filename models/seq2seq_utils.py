import numpy as np
import tensorflow as tf
from tensorflow.python.platform import gfile

from models.seq2seq import Seq2SeqModel
from configs.config import FLAGS, BUCKETS
from tf_seq2seq_chatbot.lib import data_utils



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



