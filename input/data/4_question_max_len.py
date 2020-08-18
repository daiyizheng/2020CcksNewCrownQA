#!/usr/bin/env python3
# encoding: utf-8
'''
@author: daiyizheng: (C) Copyright 2017-2019, Personal exclusive right.
@contact: 387942239@qq.com
@software: tool
@application:@file: 4_question_max_len.py
@time: 2020/8/17 上午8:37
@desc:
'''
import pandas as pd
import os
data_dir = "ner_data"
inputpaths = ["train.csv", 'dev.csv']


for i in range(len(inputpaths)):
    print("文件",inputpaths[i])
    file_path = os.path.join(data_dir, inputpaths[i])
    data = pd.read_csv(file_path)
    q_l = data['questions'].str.len().max()
    q_i = data['questions'].str.len().argmax()
    q = data['questions'][q_i]
    print("question_len",q_l, q)

    e_l = data['entitys'].str.len().max()
    e_i = data['entitys'].str.len().argmax()
    e = data['entitys'][e_i]
    print("entity_len", e_l, e)

    r_l = data['relations'].str.len().max()
    r_i = data['relations'].str.len().argmax()
    r = data['relations'][r_i]
    print("relation_len", r_l, r)


"""
question_len 53 电影《猫鼠游戏》讲诉了一个诈骗天才从FBI历史上最年轻的通缉犯到FBI金融安全顾问的故事，该角色的原型是？
entity_len 70 ['<科学家_（从事科学研究的人群）>', '<物理学家_（探索、研究物理学的科学家）>', '<数学家_（数学家（世界著名数学家））>']
relation_len 45 ['<发行商>', '<中文名>', '"国"', '<中文名称>', '<总部地点>']
文件 dev.csv
question_len 54 对于出现的剧烈运动或强体力劳动后血尿、不稳定性心绞和一过性肉眼血尿这些症状，可以通过怎样的检查项目检测病情？
entity_len 49 ['<急性淋巴细胞性白血病>', '<骨髓单核细胞白血病>', '<水痘-带状疱疹性葡萄膜炎>']
relation_len 25 ['<风险因子（英语：Riskfactor）>']
"""

"""
对于ner 任务　max_len 56
"""