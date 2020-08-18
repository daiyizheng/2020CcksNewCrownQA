#!/usr/bin/env python3
# encoding: utf-8
'''
@author: daiyizheng: (C) Copyright 2017-2019, Personal exclusive right.
@contact: 387942239@qq.com
@software: tool
@application:@file: 5_generate_smi.py
@time: 2020/8/18 上午12:32
@desc:
'''
import pandas as pd
import re
import random

data_dir = 'CCKS2020'
smi_dir = "sim_data"
data_type = "train"
# data_type = "dev"
target = "./ner_data/"+data_type+".csv"
attribute_classify_sample = []

# count the number of attribute
testing_df = pd.read_csv(target, encoding='utf-8')
testing_df['attribute'] = testing_df['relations'].apply(lambda x: re.sub("\]|\[|'|>|<|", "", x))
attribute_list = testing_df['attribute'].tolist()
print(len(set(attribute_list)))
print(testing_df.head())

# construct sample
for row in testing_df.index:
    question, pos_att = testing_df.loc[row][['questions', 'attribute']]
    question = question.strip()
    pos_att = pos_att.strip()
    # random.shuffle(attribute_list)    the complex is big
    # neg_att_list = attribute_list[0:5]
    attribute_classify_sample.append([question, pos_att, '1'])
    n = 0
    while n!=5:
        """采集负例"""
        neg_att_list = random.sample(attribute_list, 1)
        neg_att_sample = [[question, neg_att, '0'] for neg_att in neg_att_list if neg_att != pos_att]
        if neg_att_sample:
            attribute_classify_sample.extend(neg_att_sample)
            n += 1
    # print(attribute_classify_sample)

seq_result = [str(lineno) + '\t' + '\t'.join(line) for (lineno, line) in enumerate(attribute_classify_sample)]


with open("./sim_data/"+data_type+".txt", "w", encoding='utf-8') as f:
    f.write("\n".join(seq_result))
