import numpy as np

np.random.seed(1337)

from models.LSTM import *
from keras.preprocessing import sequence
# from gensim.models import Word2Vec
import sys


# def load_emb_mat():
#     w2v = Word2Vec.load(pjoin(SAVE_DATA_DIR, "word_emb_size100wind5iter5"))
#
#     embedding_matrix = np.zeros((LSTM_vocab_size+1, LSTM_embedding_size))
#     for index in range(1, LSTM_vocab_size+1):
#         embedding_matrix[index] = w2v[str(index+2)]
#
#     return embedding_matrix

def train(X_train, y_train, X_test, y_test):
    print(SAVE_DATA_DIR)

    print('Pad sequences (samples x time)')
    X_train = sequence.pad_sequences(X_train, maxlen=LSTM_max_len)
    X_test = sequence.pad_sequences(X_test, maxlen=LSTM_max_len)
    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)

    print('\nBuild model...')
    # model = create_model_lstm(embedding_trainable=True)#, embedding_matrix=load_emb_mat())
    model = create_model_lstm()

    print('\nTrain...')
    # print model.get_weights()[1][0]

    for i in xrange(5):
        print("\ni = %d"%i)

        # for _ in xrange(5):
        #     print np.random.choice([1, 2, 4, 5, 6, 7, 8, 9])
        model.fit(X_train, y_train, nb_epoch=10, batch_size=LSTM_batch_size, validation_data=[X_test, y_test])
        model.save_weights(pjoin(SAVE_DATA_DIR, "lstm_model_%d.h5"%(i*10)))


def predict(X_test, y_test, mode_name, analysis_mode=False):
    X_test = sequence.pad_sequences(X_test, maxlen=LSTM_max_len)
    print('X_test shape:', X_test.shape)

    model = create_model_lstm()
    model.load_weights(pjoin(SAVE_DATA_DIR, mode_name))

    if not analysis_mode:
        score, acc = model.evaluate(X_test, y_test,
                                    batch_size=LSTM_batch_size)
        print('Test loss:', score)
        print('Test accuracy:', acc)

    else:
        predict_y = model.predict(X_test)

        ans = {}
        for predict, test in zip(predict_y, y_test):
            # if float(predict) <= 0.28 or float(predict) > 0.5 and float(predict) <= 0.6:
            if float(predict) < 0.5:
                p_t = (0, int(test))
            else:
                p_t = (1, int(test))
            if p_t in ans:
                ans[p_t] += 1
            else:
                ans[p_t] = 1
        print ans

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
