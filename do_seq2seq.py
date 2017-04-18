import os
import sys

#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf

from lib.train_seq2seq import train
from lib.test_seq2seq import predict


def main(_):
    mode = "t"
    if mode == "t":
        train()
    else:
        predict()

if __name__ == "__main__":
    tf.app.run()
