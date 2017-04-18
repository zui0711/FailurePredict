import numpy as np
import random
import os.path

np.random.seed(1337)

from keras.preprocessing import sequence
from models.LSTM import *
from gensim.models import Word2Vec


def load_data(seq2seq_vocab_size):
    X_train = []
    y_train = []
    X_test = []
    y_test = []

    #with open(filep+"data/train_encode.ids176.txt") as f:
    # name = "encode.ids" + str(vocab_size) + ".txt"
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
        for n in nor[:8000]:
            X_train.append([int(nn)-2 for nn in n.strip().split()])
            y_train.append(0)
        for e in err[:8000]:
            X_train.append([int(ee)-2 for ee in e.strip().split()])
            y_train.append(1)

        t = zip(X_train, y_train)
        random.shuffle(t)
        for i, elem in enumerate(t):
            X_train[i], y_train[i] = elem



    # with open(pjoin(SAVE_DATA_DIR, "test", name), "rb") as f, \
    #         open(pjoin(SAVE_DATA_DIR, "test", "labels.txt"), "rb") as fl:
    name = "results(%d, %d).ids%d.txt_312300" % (LSTM_max_len, LSTM_max_len, seq2seq_vocab_size)
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

        for n in nor[:3000]:
            X_test.append([int(nn)-2 for nn in n.strip().split()])
            y_test.append(0)
        for e in err[:3000]:
            X_test.append([int(ee)-2 for ee in e.strip().split()])
            y_test.append(1)

        t = zip(X_test, y_test)
        random.shuffle(t)
        for i, elem in enumerate(t):
            X_test[i], y_test[i] = elem

    return (X_train, y_train), (X_test, y_test)


def train():
    print(SAVE_DATA_DIR)
    # w2v = Word2Vec.load(pjoin(SAVE_DATA_DIR, "word_emb_size100wind5iter5"))

    # embedding_matrix = np.zeros((LSTM_vocab_size+1, LSTM_embedding_size))
    #
    # for index in range(1, LSTM_vocab_size+1):
    #     embedding_matrix[index] = w2v[str(index+2)]

    (X_train, y_train), (X_test, y_test) = load_data(seq2seq_vocab_size)
    # xx = {}

    # for line in X_train:
    #     for x in line:
    #         if x in xx:
    #             xx[x] += 1
    #         else:
    #             xx[x] = 1
    # for line in X_test:
    #     for x in line:
    #         if x in xx:
    #             xx[x] += 1
    #         else:
    #             xx[x] = 1
    # print xx
    # print len(xx)


    print('Pad sequences (samples x time)')
    X_train = sequence.pad_sequences(X_train, maxlen=LSTM_max_len)
    X_test = sequence.pad_sequences(X_test, maxlen=LSTM_max_len)
    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)

    print('\nBuild model...')
    model = create_model(embedding_trainable=True)#, embedding_matrix=embedding_matrix)

    # try using different optimizers and different optimizer configs
    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    if not os.path.exists(pjoin(SAVE_DATA_DIR, "lstm_model.h5")):

        score, acc = model.evaluate(X_test, y_test,
                                    batch_size=LSTM_batch_size)
        print('Test loss:', score)
        print('Test accuracy:', acc)
        # predict_y = model.predict(X_test)
        #
        # ans = [{}, {}, {}, {}, {}]
        # for predict, test in zip(predict_y, y_test):
        #     for i in xrange(len(ans)):
        #         p_t = (int(predict+0.5+0.1*i), int(test))
        #         if p_t in ans[i]:
        #             ans[i][p_t] += 1
        #         else:
        #             ans[i][p_t] = 1
        # for i in xrange(len(ans)):
        #     print "predict, test", ans[i]

        print('\nTrain...')

        # for i in xrange(20):
        model.fit(X_train, y_train, batch_size=LSTM_batch_size, nb_epoch=40, validation_data=[X_test, y_test],
                  shuffle=True)
        model.save_weights(pjoin(SAVE_DATA_DIR, "lstm_model.h5"))

    else:
        model.load_weights(pjoin(SAVE_DATA_DIR, "lstm_model.h5"))
        score, acc = model.evaluate(X_test, y_test,
                                    batch_size=LSTM_batch_size)
        print('Test loss:', score)
        print('Test accuracy:', acc)



    # predict_y = model.predict(X_test)

        # predict, test
        # ne = []
        # ee = []
        # en = []
        # nn = []
        # for i, elem in enumerate(y_test):
        #     if elem == 0:
        #         if predict_y[i] > 0.5:
        #             en.append(predict_y[i])
        #         else:
        #             nn.append(predict_y[i])
        #     else:
        #         if predict_y[i] < 0.5:
        #             ne.append(predict_y[i])
        #         else:
        #             ee.append(predict_y[i])
        # ans = {}
        # for predict, test in zip(predict_y, y_test):
        #     if float(predict) <= 0.28 or float(predict) > 0.5 and float(predict) <= 0.6:
        #         p_t = (0, int(test))
        #     else:
        #         p_t = (1, int(test))
        #     if p_t in ans:
        #         ans[p_t] += 1
        #     else:
        #         ans[p_t] = 1
        # print ans
        #
        #
        # ans = [{}, {}, {}, {}, {}]
        # for predict, test in zip(predict_y, y_test):
        #     for i in xrange(len(ans)):
        #         p_t = (int(predict + 0.5 + 0.1 * i), int(test))
        #         if p_t in ans[i]:
        #             ans[i][p_t] += 1
        #         else:
        #             ans[i][p_t] = 1
        # for i in xrange(len(ans)):
        #     print "predict, test", ans[i]

if __name__ == "__main__":
    train()