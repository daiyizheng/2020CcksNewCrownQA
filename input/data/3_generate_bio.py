#!/usr/bin/env python3
# encoding: utf-8
'''
@author: daiyizheng: (C) Copyright 2017-2019, Personal exclusive right.
@contact: 387942239@qq.com
@software: tool
@application:@file: 3_generate_bio.py
@time: 2020/8/16 下午8:00
@desc:
'''

"""
通过 NLPCC2020 中的原始数据，构建用来训练NER的样本集合
构造NER训练集，实体序列标注，训练BERT+CRF
数据标记BIO
"""
import os
import pickle


def find_lcsubstr(s1, s2):
    """
    求最大长度共字符串
    :param s1:
    :param s2:
    :return:
    """
    m=[[0 for i in range(len(s2)+1)] for j in range(len(s1)+1)] #生成0矩阵，为方便后续计算，比字符串长度多了一列
    mmax=0  #最长匹配的长度
    p=0 #最长匹配对应在s1中的最后一位
    for i in range(len(s1)):
        for j in range(len(s2)):
            if s1[i]==s2[j]:
                m[i+1][j+1]=m[i][j]+1
            if m[i+1][j+1]>mmax:
                mmax=m[i+1][j+1]
                p=i+1
    return s1[p-mmax:p]

def GetXY(question,entity):
    """
    将question 转为char , 标注bio 格式
    :param question:
    :param entity:
    :return:
    """
    question_list = list(question)
    question_bio = ["O"] * len(question_list)
    for e in entity:
        #得到实体名和问题的最长连续公共子串
        e = find_lcsubstr(e, question)
        if e in question:
            begin = question.index(e)
            end = begin + len(e)
            question_bio[begin] = "B-LOC"
            for i in range(begin+1, end):
                question_bio[i] ="I-LOC"
    return question_list, question_bio

def GenerateBio(questions, entitys, path):
    """
    保存txt 格式bio
    :param questions:
    :param entitys:
    :param path:
    :return:
    """
    with open(path, 'w', encoding='utf-8') as f:
        for i in range(len(questions)):
            question_list, question_bio = GetXY(questions[i], entitys[i])
            assert len(question_list) == len(question_bio), "句子和bio标签长度不等:{}".format(questions[i])
            for i in range(len(question_list)):
                f.write(question_list[i]+"\t"+question_bio[i])
                f.write("\n")
            f.write('\n')

def SaveCsv(questions, entitys, relations, answer, csv_path):
    """
    文件保存csv
    :param question:
    :param e_str:
    :param r_str:
    :param a_str:
    :return:
    """
    import pandas as pd
    entitys_c = [list(set(e_item)) for e_item in entitys]
    relations_c = [list(set(r_item)) for r_item in relations]
    q_all = list(zip(questions, entitys_c, relations_c, answer))
    df = pd.DataFrame(q_all, columns=["questions", "entitys", "relations", "answer"])
    df.to_csv(csv_path, encoding='utf-8', index=False)




data_dir = "CCKS2020"
ner_dir = 'ner_data'
input_name_data = ['corpus_train.pkl', 'corpus_dev.pkl']
output_dir = 'ner_data'
output_name_data = ['train.txt', 'dev.txt']
for i in range(len(input_name_data)):
    inputpath = os.path.join(data_dir, input_name_data[i])
    outputpath = os.path.join(ner_dir, output_name_data[i])
    corpus = pickle.load(open(inputpath, 'rb'))
    questions = [corpus[i]['question'] for i in range(len(corpus))]
    entitys = [corpus[i]['gold_entitys'] for i in range(len(corpus))]
    GenerateBio(questions, entitys, outputpath)
    print("{} data done".format(output_name_data[i]))
    relations = [corpus[i]['gold_relations'] for i in range(len(corpus))]
    answer = [corpus[i]['answer'] for i in range(len(corpus))]
    csv_path = os.path.join(ner_dir, output_name_data[i].split('.')[0]+'.csv')
    SaveCsv(questions, entitys, relations, answer, csv_path)

