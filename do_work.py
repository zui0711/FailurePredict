from lib.data_utils import prepare_encode_decode_data
from configs.data_config import *


prepare_encode_decode_data(prepare_data_source_path,
                           prepare_data_source_file,
                           prepare_data_save_path,
                           prepare_data_label,
                           encode_decode_window,
                           encode_decode_gap,
                           encode_decode_step)


#
# tokenize(path,
#          )
#
# seq2seq_train()
#
# seq2seq_predict()
#
# lstm_classification()
