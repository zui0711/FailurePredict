from lib.data_utils import *
from configs.data_config import *


prepare_encode_decode_data(prepare_data_source_path,
                           prepare_data_source_file,
                           prepare_data_save_path,
                           prepare_data_label,
                           encode_decode_window,
                           encode_decode_gap,
                           encode_decode_step)

set_train_test(prepare_data_save_path, prepare_data_label, encode_decode_window, encode_decode_gap, encode_decode_step)

prepare_dialog_data(SAVE_DATA_DIR, LSTM_vocab_size)

#
# tokenize(path,
#          )
#
# seq2seq_train()
#
# seq2seq_predict()
#
# lstm_classification()
