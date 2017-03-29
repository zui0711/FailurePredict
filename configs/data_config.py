# coding=utf-8
from os.path import join as pjoin
import tensorflow as tf

ERRORNAME = ["USER_CONGESTION",
             "GTPC_TUNNEL_PATH_BROKEN",
             "PROCESS_CPU",
             "SYSTEM_FLOW_CTRL",
             "EPU_PORT_CONGESTION"]

ERRORRECOVERY = ["USER_CONGESTION_RECOVERY",
                 "GTPC_TUNNEL_PATH_RECOVERY",
                 "PROCESS_CPU_RECOVERY",
                 "SYSTEM_FLOW_CTRL_RECOVERY",
                 "EPU_PORT_CONGESTION_RECOVERY"]

encode_decode_window = 15
encode_decode_gap = 5000
encode_decode_step = 10

LSTM_vocab_size = 164
LSTM_max_len = 120
LSTM_embedding_size = 128
LSTM_batch_size = 128

prepare_data_source_path = "/media/workserv/498ee660-1fc8-40e8-bb02-f0a626cbfe93/jwl/PycharmProjects/FailureAnalysis/data/network_diagnosis_data"
prepare_data_source_file = "BaseLine-BigData_1kUE_20ENB_paging-Case_Group_1-Case_1"
prepare_data_label = "Paging"
prepare_data_save_path = "/media/workserv/498ee660-1fc8-40e8-bb02-f0a626cbfe93/jwl/PycharmProjects/ALL_DATA/FailurePredict"

SAVE_DATA_DIR = pjoin(prepare_data_save_path, prepare_data_label,
                      "_".join([str(encode_decode_window), str(encode_decode_gap), str(encode_decode_step)]))
TEST_DATASET_PATH = pjoin(SAVE_DATA_DIR, "test", "encode.ids164.txt")

tf.app.flags.DEFINE_string('data_dir', SAVE_DATA_DIR, 'data directory')
tf.app.flags.DEFINE_string('model_dir', SAVE_DATA_DIR + '/nn_models', 'Train directory')
tf.app.flags.DEFINE_string('results_dir', SAVE_DATA_DIR + '/results', 'Train directory')

tf.app.flags.DEFINE_float('learning_rate', 0.5, 'Learning rate.')
tf.app.flags.DEFINE_float('learning_rate_decay_factor', 0.99, 'Learning rate decays by this much.')
tf.app.flags.DEFINE_float('max_gradient_norm', 5.0, 'Clip gradients to this norm.')
tf.app.flags.DEFINE_integer('batch_size', 64, 'Batch size to use during training.')

tf.app.flags.DEFINE_integer('vocab_size', LSTM_vocab_size, 'Dialog vocabulary size.')
tf.app.flags.DEFINE_integer('hidden_size', 128, 'Size of each model layer.')
tf.app.flags.DEFINE_integer('embedding_size', 128, 'Size of embedding.')
tf.app.flags.DEFINE_integer('num_layers', 1, 'Number of layers in the model.')

tf.app.flags.DEFINE_integer('max_train_data_size', 0, 'Limit on the size of training data (0: no limit).')
tf.app.flags.DEFINE_integer('steps_per_checkpoint', 200, 'How many training steps to do per checkpoint.')

FLAGS = tf.app.flags.FLAGS

# We use a number of buckets and pad to the closest one for efficiency.
# See seq2seq_model.Seq2SeqModel for details of how they work.
#BUCKETS = [(5, 10), (10, 15), (20, 25), (40, 50)]
# BUCKETS = [(80, 80), (120, 120), (150, 150)]
BUCKETS = [(360, 360)]

# 最原始数据
# source_cut_data_path = data_in_path
# save_cut_data_path = data_in_path
#
# # 从clean.txt中得到输入输出,即编解码对
# get_encode_decode_data_path = "/media/workserv/498ee660-1fc8-40e8-bb02-f0a626cbfe93/jwl/PycharmProjects/FailureAnalysis/data/network_diagnosis_data" + "cut_recovery_10/Paging"
# save_encode_decode_data_path = data_in_path

# 分解编解码对


# 使用编解码对进行训练,用

# 对encode,decode进行tokenize


