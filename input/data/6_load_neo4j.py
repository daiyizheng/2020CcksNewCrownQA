#!/usr/bin/env python3
# encoding: utf-8
'''
@author: daiyizheng: (C) Copyright 2017-2019, Personal exclusive right.
@contact: 387942239@qq.com
@software: tool
@application:@file: 6_load_neo4j.py
@time: 2020/8/18 上午10:01
@desc:
'''

import csv
import json
from tqdm import tqdm
"""
##导入neo4j数据库
./neo4j-admin import --database=pkubase.db 
--nodes "/home/daiyizheng/文档/NLP-NER-projet/CCKS -2020-ckbqa/data/pre-data/node.csv" 
--relationships "/home/daiyizheng/文档/NLP-NER-projet/CCKS -2020-ckbqa/data/pre-data/relation.csv" 
--ignore-extra-columns=true 
--ignore-missing-nodes=true 
--ignore-duplicate-nodes=true
"""
import pickle
def gen_node_file():
    file = open(r'/home/daiyizheng/.cache_data/CCKS/2020/CCKS 2020新冠知识图谱构建与问答评测4新冠知识图谱问答评测/pkubase-complete2.txt', 'r', encoding='utf-8').readlines()
    print('node_file 数据库原始文件读取完成')
    csvf = open('./db_data/node.csv', 'w', newline='', encoding='utf-8')

    w = csv.writer(csvf)
    w.writerow(("id:ID","name",":LABEL"))
    idx = 0
    entity_dic = dict()
    print(len(file))

    for i in tqdm(range(len(file))):
        #         if '<类型>' in file[i]:
        #             continue
        # 2019.8.30这次导入将实体的类型属性也导入数据库中
        try:
            entity1 = file[i].split('\t')[0]
            if entity1 not in entity_dic:
                idx += 1
                entity_dic[entity1] = idx
                w.writerow((str(idx), entity1, 'Entity'))

            entity2 = file[i].split('\t')[2].rstrip(' .\n')
            if entity2 not in entity_dic:
                idx += 1
                entity_dic[entity2] = idx
                w.writerow((str(idx), entity2, 'Entity'))
        except Exception as e:
            print("node", i, file[i])

    print(len(entity_dic))
    csvf.close()
    return entity_dic

entity_dic = gen_node_file()

file = open(r'/home/daiyizheng/.cache_data/CCKS/2020/CCKS 2020新冠知识图谱构建与问答评测4新冠知识图谱问答评测/pkubase-complete2.txt','r',encoding='utf-8').readlines()
print(len(entity_dic))
print("relation 开始")
csvf = open('./db_data/relation.csv','w',newline='',encoding = 'utf-8')
w = csv.writer(csvf)
w.writerow((":START_ID",":END_ID",":TYPE","name"))

for i in tqdm(range(len(file))):
#     if '<类型>' in file[i]:
#         continue
#2019.8.30更新
    try:
        entity1 = file[i].split('\t')[0]
        entity2 = file[i].split('\t')[2].rstrip(' .\n')
        relation = file[i].split('\t')[1]

        w.writerow((str(entity_dic[entity1]),str(entity_dic[entity2]),'Relation',relation))
    except Exception as e:
        print("relation", i, file[i])

csvf.close()



