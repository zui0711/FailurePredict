# from keras.backend.tensorflow_backend import set_session

import numpy as np
np.random.seed(1337)

import os

from lib.lstm_classifcation import *


def load_data(seq2seq_vocab_size, seq2seq_epoch):
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    name = "decode.ids%d.txt"%seq2seq_vocab_size
    print name

    with open(pjoin(SAVE_DATA_DIR, "train", name), "rb") as f,\
            open(pjoin(SAVE_DATA_DIR, "train", "labels.txt"), "rb") as fl:
        con = f.readlines()
        conl = fl.readlines()
        f.close()
        fl.close()

        nor = []
        err = []

        print(len(con))
        for i, line in enumerate(con):
            if conl[i].strip() == "Normal":
                nor.append(line)
            else:
                err.append(line)

        print("train: nor -> %d, err -> %d"%(len(nor), len(err)))
        for n in nor[:len(err)]:
            X_train.append([int(nn)-2 for nn in n.strip().split()])
            y_train.append(0)
        for e in err:
            X_train.append([int(ee)-2 for ee in e.strip().split()])
            y_train.append(1)

        t = zip(X_train, y_train)
        np.random.shuffle(t)
        for i, elem in enumerate(t):
            X_train[i], y_train[i] = elem

    # with open(pjoin(SAVE_DATA_DIR, "test", name), "rb") as f, \
    #         open(pjoin(SAVE_DATA_DIR, "test", "labels.txt"), "rb") as fl:
    name = "results(%d, %d).ids%d.%d" % (LSTM_max_len, LSTM_max_len, seq2seq_vocab_size, seq2seq_epoch)
    with open(pjoin(SAVE_DATA_DIR, "results", name), "rb") as f, \
            open(pjoin(SAVE_DATA_DIR, "test", "labels.txt"), "rb") as fl:
        con = f.readlines()
        conl = fl.readlines()
        f.close()
        fl.close()

        nor = []
        err = []

        print(len(con))
        for i, line in enumerate(con):
            if conl[i].strip() == "Normal":
                nor.append(line)
            else:
                err.append(line)
        print("test: nor -> %d, err -> %d"%(len(nor), len(err)))

        for n in nor[:len(err)]:
            X_test.append([int(nn)-2 for nn in n.strip().split()])
            y_test.append(0)
        for e in err:
            X_test.append([int(ee)-2 for ee in e.strip().split()])
            y_test.append(1)

        t = zip(X_test, y_test)
        np.random.shuffle(t)
        for i, elem in enumerate(t):
            X_test[i], y_test[i] = elem

    return (X_train, y_train), (X_test, y_test)

# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# set_session(tf.Session(config=config))

# for n in range(0, 50, 10):
print("\nStart...")
# print("n = %d"%n)
(X_train, y_train), (X_test, y_test) = load_data(seq2seq_vocab_size, 5000)

mode_name = "lstm_model_20.h5"
if not os.path.exists(pjoin(SAVE_DATA_DIR, mode_name)):
    train(X_train, y_train, X_test, y_test)
else:
    predict(X_test, y_test, mode_name)
