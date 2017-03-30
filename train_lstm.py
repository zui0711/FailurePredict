import numpy as np
import random

np.random.seed(1337)

from keras.preprocessing import sequence
from models.LSTM import *

def load_data(vocab_size):
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    #with open(filep+"data/train_encode.ids176.txt") as f:
    # name = "encode.ids" + str(vocab_size) + ".txt"
    name = "decode.ids%d.txt"%vocab_size

    with open(pjoin(SAVE_DATA_DIR, "train", name), "rb") as f,\
            open(pjoin(SAVE_DATA_DIR, "train", "labels.txt"), "rb") as fl:
        con = f.readlines()
        conl = fl.readlines()

        nor = []
        err = []

        print(len(con))
        for i, line in enumerate(con):
            if conl[i].strip() == "Normal":
                nor.append(line)
            else:
                err.append(line)

        print("train: nor -> %d, err -> %d"%(len(nor), len(err)))
        # for i in xrange(16000):
        #     X_train.append([int(n) for n in nor[i].strip().split()])
        #     y_train.append(0)
        # for i in xrange(16000):
        #     X_train.append([int(n) for n in err[i].strip().split()])
        #     y_train.append(1)
        idxs = range(32000)
        random.shuffle(idxs)
        for num in idxs:
            if num < 16000:
                X_train.append([int(n)-2 for n in nor[num].strip().split()])
                y_train.append(0)
            else:
                X_train.append([int(n)-2 for n in err[num-16000].strip().split()])
                y_train.append(1)

    # with open(pjoin(SAVE_DATA_DIR, "train", "labels.txt"), "rb") as f:
    #     con = f.readlines()
    #     print(len(con))
    #     for line in con[:60000]:
    #         if line.strip() == "Normal":
    #             y_train.append(0)
    #         else:
    #             y_train.append(1)

    # with open(filep+"BUCKET150/test_decode_predict.ids176.txt") as f:
    # with open(pjoin(SAVE_DATA_DIR, "test", name), "rb") as f:
    #     con = f.readlines()
    #     print(len(con))
    #     for line in con[:4000]:
    #         X_test.append([int(n) for n in line.strip().split()])
    # with open(pjoin(SAVE_DATA_DIR, "test", "labels.txt"), "rb") as f:
    #     con = f.readlines()
    #     print(len(con))
    #     for line in con[:4000]:
    #         if line.strip() == "Normal":
    #             y_test.append(0)
    #         else:
    #             y_test.append(1)

    # name = "results(%d, %d).ids%d.txt"%(LSTM_max_len, LSTM_max_len, vocab_size)
    # with open(pjoin(FLAGS.results_dir, name), "rb") as f, \
    with open(pjoin(SAVE_DATA_DIR, "test", name), "rb") as f, \
            open(pjoin(SAVE_DATA_DIR, "test", "labels.txt"), "rb") as fl:
        con = f.readlines()
        conl = fl.readlines()

        nor = []
        err = []

        print(len(con))
        for i, line in enumerate(con):
            if conl[i].strip() == "Normal":
                nor.append(line)
            else:
                err.append(line)
        print("test: nor -> %d, err -> %d"%(len(nor), len(err)))

        idxs = range(8000)
        random.shuffle(idxs)
        for num in idxs:
            if num < 4000:
                X_test.append([int(n)-2 for n in nor[num].strip().split()])
                y_test.append(0)
            else:
                X_test.append([int(n)-2 for n in err[num-4000].strip().split()])
                y_test.append(1)

        # for i in xrange(4000):
        #     X_test.append([int(n) for n in nor[i].strip().split()])
        #     y_test.append(0)
        # for i in xrange(4000):
        #     X_test.append([int(n) for n in err[i].strip().split()])
        #     y_test.append(1)

    return (X_train, y_train), (X_test, y_test)


def train():
    print(SAVE_DATA_DIR)
    (X_train, y_train), (X_test, y_test) = load_data(LSTM_vocab_size)
    xx = {}

    for line in X_train:
        for x in line:
            if x in xx:
                xx[x] += 1
            else:
                xx[x] = 1
    for line in X_test:
        for x in line:
            if x in xx:
                xx[x] += 1
            else:
                xx[x] = 1
    print xx


    print(len(X_train), 'train sequences')
    print(len(X_test), 'test sequences')

    print('Pad sequences (samples x time)')
    X_train = sequence.pad_sequences(X_train, maxlen=LSTM_max_len)
    X_test = sequence.pad_sequences(X_test, maxlen=LSTM_max_len)
    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)

    print('Build model...')
    model = create_model()

    # try using different optimizers and different optimizer configs
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    score, acc = model.evaluate(X_test, y_test,
                                batch_size=LSTM_batch_size)
    print('Test loss:', score)
    print('Test accuracy:', acc)
    print('Train...')

    model.fit(X_train, y_train, batch_size=LSTM_batch_size, nb_epoch=50, validation_data=[X_test, y_test], shuffle=True)
    # model.fit(X_train, y_train, batch_size=LSTM_batch_size, nb_epoch=50, validation_split=0.2, shuffle=True)
    #          validation_data=(X_test, y_test))
    score, acc = model.evaluate(X_test, y_test,
                                batch_size=LSTM_batch_size)
    print('Test loss:', score)
    print('Test accuracy:', acc)

if __name__ == "__main__":
    train()