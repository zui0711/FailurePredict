import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


path = "/media/workserv/Seagate Backup Plus Drive/ALL_DATA/FailurePredict/Paging/analysis/"
data1 = pd.read_excel(path + "diff_step.xls")
# data2 = pd.read_excel(path + "50_2000_10_2.xls")

x1 = np.array(data1.iloc[:, 1])
x2 = np.array(data1.iloc[:, 4])
# x3 = np.array(data1.iloc[:, 7])

lenx1 = len(x1) - len(x1[np.isnan(x1)])
lenx2 = len(x2) - len(x2[np.isnan(x2)])
# lenx3 = len(x3) - len(x3[np.isnan(x3)])
tlen = min([lenx1, lenx2])
# tlen = min([lenx1, lenx2, lenx3])

print tlen

# print aaa

xl = range(5000, 5000*tlen+5000, 5000)

plt.plot(xl, x1[:tlen], "--")
plt.plot(xl, x2[:tlen], "-.^")
# plt.plot(xl, x3[:tlen], "-")
plt.xlabel("epoch")
plt.ylabel("WER")
# plt.legend(["lwin=50(with sampling)", "lwin=30(with sampling)", "lwin=30(without sampling)"])
plt.legend(["gap=5000", "gap=2000", "gap=1000"])
# plt.title("WER with different wlen")
plt.show()