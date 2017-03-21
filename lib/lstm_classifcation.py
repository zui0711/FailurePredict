'''Trains a LSTM on the IMDB sentiment classification task.
The dataset is actually too small for LSTM to be of any advantage
compared to simpler, much faster methods such as TF-IDF + LogReg.
Notes:
- RNNs are tricky. Choice of batch size is important,
choice of loss and optimizer is critical, etc.
Some configurations won't converge.
- LSTM loss decrease patterns during training can be quite different
from what you see with CNNs/MLPs/etc.
'''
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM

max_features = 176
maxlen = 150  # cut texts after this number of words (among top max_features most common words)
batch_size = 128
train_n = 60000
test_n = 4000

filep = "line10_label_train15000/"

print('Loading data...')
#(X_train, y_train), (X_test, y_test) = imdb.load_data(nb_words=max_features)

def load_data():
    X_train = []
    y_train = []
    X_test = []
    y_test = []    
    
    #with open(filep+"data/train_encode.ids176.txt") as f:
    with open(filep+"data/train_decode.ids176.txt") as f:
        for line in f.readlines()[:train_n]:
            X_train.append([int(n) for n in line.strip().split()])
    with open(filep+"data/train_n2l.txt") as f:
        for line in f.readlines()[:train_n]:
            if line.strip() == "Normal":
                y_train.append(0)
            else:
                y_train.append(1)

    #with open(filep+"BUCKET150/test_decode_predict.ids176.txt") as f:
    with open(filep+"data/test_decode.ids176.txt") as f:
        for line in f.readlines()[:test_n]:
            X_test.append([int(n) for n in line.strip().split()])
    with open(filep+"data/test_n2l.txt") as f:
        for line in f.readlines()[:test_n]:
            if line.strip() == "Normal":
                y_test.append(0)
            else:
                y_test.append(1)
    
    return (X_train, y_train), (X_test, y_test)
(X_train, y_train), (X_test, y_test) = load_data()
print(len(X_train), 'train sequences')
print(len(X_test), 'test sequences')

print('Pad sequences (samples x time)')
X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
print('X_train shape:', X_train.shape)
print('X_test shape:', X_test.shape)

print('Build model...')
model = Sequential()
model.add(Embedding(max_features, 200, dropout=0.05))
model.add(LSTM(200, dropout_W=0.05, dropout_U=0.05))  # try using a GRU instead, for fun
model.add(Dense(1))
model.add(Activation('sigmoid'))

# try using different optimizers and different optimizer configs
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

score, acc = model.evaluate(X_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)
print('Train...')

model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=5,validation_split=0.1)
#          validation_data=(X_test, y_test))
score, acc = model.evaluate(X_test, y_test,
                            batch_size=batch_size)
print('Test score:', score)
print('Test accuracy:', acc)
