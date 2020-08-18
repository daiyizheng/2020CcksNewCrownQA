# CCKS 2020：新冠知识图谱构建与问答评测（四）新冠知识图谱问答评测


## 依赖版本
transformers==2.1.1
torch==1.1
```shell script
#运行ner 任务
python Ner_main 
--data_dir
./input/data/ner_data
--vob_file
/home/daiyizheng/.cache/torch/transformers/bert-pretrainmodel/bert/bert-base-chinese/vocab.txt
--model_config
/home/daiyizheng/.cache/torch/transformers/bert-pretrainmodel/bert/bert-base-chinese/config.json
--output
./output
--max_seq_length
56
--do_train
--train_batch_size
12
--eval_batch_size
16
--gradient_accumulation_steps
4
--num_train_epochs
15
```

```shell script
#运行SMI_ner
--data_dir
./input/data/sim_data
--vob_file
/home/daiyizheng/.cache/torch/transformers/bert-pretrainmodel/bert/bert-base-chinese/vocab.txt
--model_config
/home/daiyizheng/.cache/torch/transformers/bert-pretrainmodel/bert/bert-base-chinese/config.json
--output
./output
--max_seq_length
56
--do_train
--train_batch_size
32
--eval_batch_size
32
--gradient_accumulation_steps
1
--num_train_epochs
15
--pre_train_model
/home/daiyizheng/.cache/torch/transformers/bert-pretrainmodel/bert/bert-base-chinese/pytorch_model.bin
```

