#!/usr/bin/env python3
# encoding: utf-8
'''
@author: daiyizheng: (C) Copyright 2017-2019, Personal exclusive right.
@contact: 387942239@qq.com
@software: tool
@application:@file: 1_split_data.py
@time: 2020/8/16 下午6:02
@desc:
'''
import os
import code
import re
data_dir = "CCKS2020"
import random
input_file_name = ["task1-4_train_2020.txt"]
output_file_name = ["train.txt", "dev.txt"]
train_ratio = 0.8

if len(input_file_name)==1:
    path = os.path.join(data_dir, input_file_name[0])
    with open(path, 'r', encoding='utf-8') as f:

        questions = []
        sparsql = []
        answers = []
        for index, line in enumerate(f.readlines()):
            line = line.strip()
            if index%4==0:
                questions.append(line)

            elif index%4==1:
                sparsql.append(line)

            elif index%4==2:
                answers.append(line)

        assert len(questions) == len(sparsql) == len(answers)
        files = list(zip(questions, sparsql, answers))
        random.shuffle(files)

        file = []
        for index, item in enumerate(files):
            file.append(item[0])
            file.append(item[1])
            file.append(item[2])
            file.append('\n')

    ## shuffle
    # code.interact(local=locals())
    assert len(file)%4 == 0
    num = int(len(file)/4*0.8)*4
    train_data = file[:num]
    dev_data = file[num:]
    print("train_data", train_data[-4:])
    print("dev_data", dev_data[-4:])
    with open(os.path.join(data_dir,"train.txt"), 'w', encoding='utf-8') as ft:
        ft.write("\n".join(train_data))

    with open(os.path.join(data_dir, "dev.txt"), 'w', encoding='utf-8') as fd:
        fd.write("\n".join(dev_data))
else:
    pass


