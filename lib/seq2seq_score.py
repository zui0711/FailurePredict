import numpy as np
import nltk
import random
import time
from configs.data_config import *

random.seed(1337)

def WER_score(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split())
    """
    #build the matrix
    d = np.zeros((len(r)+1)*(len(h)+1), dtype=np.uint16).reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        for j in range(len(h)+1):
            if i == 0: d[0][j] = j
            elif j == 0: d[i][0] = i

    for i in range(1,len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)

    err_rate = float(d[len(r)][len(h)]) / len(r)
    # print d[len(r)][len(h)], err_rate
    return err_rate


def BLEU_score(r, h):
    return nltk.translate.bleu_score.sentence_bleu([r], h)


def get_score(file_r, file_h):
    with open(file_r) as fr, open(file_h) as fh:
        r = fr.readlines()
        h = fh.readlines()
        indexs = random.sample(range(len(h)), 500)
        wer = []
        bleu = []
        start_time = time.time()
        for idx in indexs:
            tr = r[idx].split()
            th = h[idx].split()
            wer.append(WER_score(tr, th))
            bleu.append(BLEU_score(tr, th))
        t = time.time() - start_time
        print("get_score: total time = %0.2f, per time = %0.2f" % (t, t / 500.))

        print("WER = %.5f, BLUE = %.5f\n" % (np.mean(wer), np.mean(bleu)))
        return np.mean(wer), np.mean(bleu)


if __name__ == '__main__':
    SAVE_DATA_DIR = pjoin("/media/workserv/Seagate Backup Plus Drive/ALL_DATA/FailurePredict", prepare_data_label,
                          "_".join([str(encode_decode_window), str(encode_decode_gap), str(encode_decode_step), "good"]))
    file_r = pjoin(SAVE_DATA_DIR, "test/decode.txt")
    file_h = pjoin(SAVE_DATA_DIR, "results/results(360, 360).txt_218300")
    get_score(file_r, file_h)