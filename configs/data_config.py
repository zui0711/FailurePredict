# coding=utf-8

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

LSTM_word_dim = 176
LSTM_max_len = 150
LSTM_embedding_dim = 200

prepare_data_source_path = "/media/workserv/498ee660-1fc8-40e8-bb02-f0a626cbfe93/jwl/PycharmProjects/FailureAnalysis/data/network_diagnosis_data"
prepare_data_source_file = "BaseLine-BigData_1kUE_20ENB_paging-Case_Group_1-Case_1"
prepare_data_label = "Paging"
prepare_data_save_path = "data"

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


