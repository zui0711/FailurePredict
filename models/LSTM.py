from configs.data_config import *

from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM
from keras.layers import Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D



def create_model():
    model = Sequential()
    model.add(Embedding(input_dim=LSTM_vocab_size-2, output_dim=LSTM_embedding_size))
    model.add(LSTM(LSTM_embedding_size, dropout_W=0.2, dropout_U=0.2))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    return model

# def create_model():
#     model = Sequential()
#     model.add(Embedding(input_dim=LSTM_vocab_size, output_dim=LSTM_embedding_size, input_length=LSTM_max_len, dropout=0.2))
#     model.add(Conv1D(128, 5, activation='relu'))
#     model.add(MaxPooling1D(5))
#     model.add(Conv1D(128, 5, activation='relu'))
#     model.add(MaxPooling1D(10))
#     model.add(Flatten())
#     model.add(Dense(100))
#     model.add(Activation('relu'))
#
#     # We project onto a single unit output layer, and squash it with a sigmoid:
#     model.add(Dense(1))
#     model.add(Activation('sigmoid'))
#     return model