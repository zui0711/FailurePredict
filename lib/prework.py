# coding=utf-8

import os
from os.path import join as pjoin
from configs.data_config import *

def cut_data(source_path,
             source_name,
             save_path,
             label,
             encode_decode_window,
             encode_decode_gap,
             encode_decode_step):
    # 将数据切分为normal,error,recovery三部分,并获取encode decode数据以及对应的标签(normal,error)
    f = open(pjoin(source_path, source_name, "clean.txt"), "rb")
    contxt = f.readlines()#[:1000000]

    filename = pjoin(save_path, "_".join([label, str(encode_decode_window), str(encode_decode_gap), str(encode_decode_step)]))
    if not os.path.exists(filename):
        os.makedirs(filename)

    count = 0
    # 文件计数器
    line_count = 0
    # 文本行数计数器
    file_empty = True
    # 是否为空文件

    ERR_flag = 0
    REC_flag = 0

    print(len(contxt))
    flags = [0 for i in xrange(len(contxt))]

    cut_start = []    # 故障开始
    cut_mid = []    # 故障结束,开始恢复
    cut_end = [-1]    # 恢复结束

    # 判断每句是否有错误
    for i, line in enumerate(contxt):
        arr = line.split()
        for word in arr:
            if word in ERRORNAME:
                flags[i] = 1
                #print(i, line)
        for word in arr:
            if word in ERRORRECOVERY:
                flags[i] = -1
                #print(i, word)

    # 标记根据error,recovery切分
    write = True
    for i, f in enumerate(flags):
        if f == 1:
            if REC_flag > ERR_flag:
                write = True
                cut_end.append(REC_flag)
            if write:
                cut_start.append(i)
                write = False
            ERR_flag = i
        elif f == -1:
            if REC_flag < ERR_flag:
                cut_mid.append(i)
            REC_flag = i

    iferr = []
    for i in range(1, len(cut_start)):
        encode_s = cut_end[i]
        encode_e = encode_s + encode_decode_window

        decode_s = encode_e + encode_decode_gap
        decode_e = decode_s + encode_decode_window

        while(decode_e < cut_start[i]):
            # print(i, encode_s)
            f = pjoin(filename, "encode")
            if not os.path.exists(f):
                os.makedirs(f)
            inf = open(pjoin(f, str(count) + ".txt"), "wb")
            for line in contxt[encode_s: encode_e]:
                #inf.write(line.strip()+" SEN_END\n")
                inf.write(line.strip() + "\n")
            f = pjoin(filename, "decode")
            if not os.path.exists(f):
                os.makedirs(f)
            outf = open(pjoin(f, str(count) + ".txt"), "wb")
            for line in contxt[decode_s: decode_e]:
                #outf.write(line.strip()+" SEN_END\n")
                outf.write(line.strip() + "\n")

            iferr.append("Normal")
            count += 1
            # update_bound(encode_s, encode_e, decode_s, decode_e)
            encode_s += encode_decode_step
            encode_e = encode_s + encode_decode_window

            decode_s = encode_e + encode_decode_gap
            decode_e = decode_s + encode_decode_window

        while(encode_e < cut_start[i]):
            # print(i, encode_s)

            inf = open(pjoin(filename, "encode", str(count) + ".txt"), "wb")
            for line in contxt[encode_s: encode_e]:
                inf.write(line)
            outf = open(pjoin(filename, "decode", str(count) + ".txt"), "wb")
            for line in contxt[decode_s: decode_e]:
                arr = line.split()
                write = True
                for word in ERRORNAME:
                    if word in arr:
                        #print(line, "ERRORNAME")
                        write = False
                        break
                if write:
                    #outf.write(line.strip()+" SEN_END\n")
                    outf.write(line.strip() + "\n")

            iferr.append("Error")
            count += 1

            encode_s += encode_decode_step
            encode_e = encode_s + encode_decode_window

            decode_s = encode_e + encode_decode_gap
            decode_e = decode_s + encode_decode_window

        print(len(iferr))
        wf = open(pjoin(filename, "labels.txt"), "wb")
        for label in iferr:
            wf.write(label+"\n")


        j = i - 1
        f = pjoin(filename, "normal")
        if not os.path.exists(f):
            os.makedirs(f)
        nf = open(pjoin(f, str(j)+".txt"), "wb")
        for line in contxt[cut_end[j]+1: cut_start[j]]:
            nf.write(line)

        f = pjoin(filename, "error")
        if not os.path.exists(f):
            os.makedirs(f)
        ef = open(pjoin(f, str(j)+".txt"), "wb")
        for line in contxt[cut_start[j]: cut_mid[j]-1]:
            ef.write(line)

        f = pjoin(filename, "recovery")
        if not os.path.exists(f):
            os.makedirs(f)
        rf = open(pjoin(f, str(j) + ".txt"), "wb")
        for line in contxt[cut_mid[j]:cut_end[j+1]]:
            rf.write(line)
