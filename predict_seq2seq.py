import os
import sys

import tensorflow as tf

from lib.test_seq2seq import predict


def main(_):
    predict()

if __name__ == "__main__":
    tf.app.run()