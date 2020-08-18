#!/usr/bin/env python3
# encoding: utf-8
'''
@author: daiyizheng: (C) Copyright 2017-2019, Personal exclusive right.
@contact: 387942239@qq.com
@software: tool
@application:@file: 2_load_corpus.py
@time: 2020/8/17 上午12:06
@desc:
'''
import os
import codecs as cs
import re
import pickle
def LoadCorpus(path):
    corpus = {}
    question_num = 0
    e1hop1_num = 0
    e1hop2_num = 0
    e2hop2_num = 0


    with cs.open(path, 'r', encoding='utf-8') as fp:
        text = fp.read().split('\n\n')[:-1]
        for i in range(len(text)):
            # 对问题进行预处理
            question = text[i].lstrip('\n').split('\n')[0]
            question = re.sub("q\d+:", "", question)
            question = re.sub('我想知道', '', question)
            question = re.sub('你了解', '', question)
            question = re.sub('请问', '', question)

            answer = text[i].lstrip('\n').split('\n')[2]
            sql = text[i].lstrip('\n').split('\n')[1]
            sql = re.findall('{.+?}', sql)[0]
            elements = re.findall('<.+?>|\".+?\"|\?\D', sql) + re.findall('\".+?\"', sql)
            #elements中包含创引号的项目可能有重复，需要去重
            new_elements = []

            for e in elements:
                if e[0] == '\"':
                    if e not in new_elements:
                        new_elements.append(e)
                else:
                    new_elements.append(e)

            elements = new_elements

            gold_entitys = []
            gold_relations = []
            for j in range(len(elements)):
                if elements[j][0]=='<' or elements[j][0]=='\"':
                    if j%3==1:
                        gold_relations.append(elements[j])
                    else:
                        gold_entitys.append(elements[j])
            gold_tuple = tuple(gold_entitys + gold_relations)
            dic = {}
            dic['question'] = question  # 问题字符串
            dic['answer'] = answer  # 问题的答案
            dic['gold_tuple'] = gold_tuple
            dic['gold_entitys'] = gold_entitys
            dic['gold_relations'] = gold_relations
            dic['sql'] = sql
            corpus[i] = dic
            if len(gold_relations) == 0:
                print(text[i])
            # 一些统计信息
            if len(gold_entitys) == 1 and len(gold_relations) == 1:
                e1hop1_num += 1
            elif len(gold_entitys) == 1 and len(gold_relations) == 2:
                e1hop2_num += 1
            elif len(gold_entitys) >= 2 and len(gold_relations) >= 2:
                e2hop2_num += 1
            elif len(gold_entitys) == 2 and len(gold_relations) < 2:
                print(elements)
                print(dic['gold_entitys'])
                print(dic['sql'])
                print('\n')

            question_num += 1
        print('语料集问题数为%d==单实体单关系数为%d====单实体双关系数为%d==双实体双关系数为%d==总比例为%.3f\n' % (question_num, e1hop1_num, e1hop2_num, e2hop2_num, (e1hop1_num + e1hop2_num + e2hop2_num) / question_num))
        return corpus




data_dir = 'CCKS2020'
inputpaths = ['train.txt', 'dev.txt']
outputpaths = ['corpus_train.pkl','corpus_dev.pkl']
corpuses = []
for i in range(len(inputpaths)):
    inputpath = os.path.join(data_dir, inputpaths[i])
    corpus = LoadCorpus(inputpath)
    outputpath = os.path.join(data_dir,outputpaths[i])
    pickle.dump(corpus, open(outputpath, 'wb'))
