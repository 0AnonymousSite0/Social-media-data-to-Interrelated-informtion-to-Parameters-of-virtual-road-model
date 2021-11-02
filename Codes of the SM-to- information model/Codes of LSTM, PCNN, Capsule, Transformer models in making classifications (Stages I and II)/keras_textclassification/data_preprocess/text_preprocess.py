# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/6/5 21:36
# @author   :Mo
# @function :data utils of text classification


# from keras_textclassification.conf.path_config import path_model_dir
# path_fast_text_model_vocab2index = path_model_dir + 'vocab2index.json'
# path_fast_text_model_l2i_i2l = path_model_dir + 'l2i_i2l.json'
from collections import Counter
from tqdm import tqdm
import pandas as pd
import numpy as np
import random
# import jieba
import json
import re
import os


__all__  = ["PreprocessText", "PreprocessTextMulti", "PreprocessSim"]

__tools__ = ["txt_read", "txt_write", "extract_chinese", "read_and_process",
             "preprocess_label_ques", "save_json", "load_json", "delete_file",
             "transform_multilabel_to_multihot"]


def txt_read(file_path, encode_type='utf-8'):
    """
      读取txt文件，默认utf8格式
    :param file_path: str, 文件路径
    :param encode_type: str, 编码格式
    :return: list
    """
    list_line = []
    try:
        file = open(file_path, 'r', encoding=encode_type)
        while True:
            line = file.readline()
            line = line.strip()
            if not line:
                break
            list_line.append(line)
        file.close()
    except Exception as e:
        print(str(e))
    finally:
        return list_line


def txt_write(list_line, file_path, type='w', encode_type='utf-8'):
    """
      txt写入list文件
    :param listLine:list, list文件，写入要带"\n" 
    :param filePath:str, 写入文件的路径
    :param type: str, 写入类型, w, a等
    :param encode_type: 
    :return: 
    """
    try:
        file = open(file_path, type, encoding=encode_type)
        file.writelines(list_line)
        file.close()

    except Exception as e:
        print(str(e))


def extract_chinese(text):
    """
      只提取出中文、字母和数字
    :param text: str, input of sentence
    :return: 
    """
    chinese_exttract = ''.join(re.findall(u"([\u4e00-\u9fa5A-Za-z0-9@._])", text))
    return chinese_exttract


def read_and_process(path):
    """
      读取文本数据并
    :param path: 
    :return: 
    """
    with open(path, 'rt' , encoding='utf-8') as f:
        lines = f.readlines()
        line_x = [extract_chinese(str(line.split(",")[0])) for line in lines]
        line_y = [extract_chinese(str(line.split(",")[1])) for line in lines]
    return line_x, line_y

    #data = pd.read_csv(path,encoding="utf-8")
    #ques = data["ques"].values.tolist()
    #labels = data["label"].values.tolist()
    #line_x = [extract_chinese(str(line).upper()) for line in labels]
    #line_y = [extract_chinese(str(line).upper()) for line in ques]
    #return line_x, line_y


def preprocess_label_ques(path):
    x, y, x_y = [], [], []
    x_y.append('label,ques\n')
    with open(path, 'r', encoding='utf-8') as f:
        while True:
            line = f.readline()
            try:
                line_json = json.loads(line)
            except:
                break
            ques = line_json['title']
            label = line_json['category'][0:2]
            line_x = " ".join([extract_chinese(word) for word in list(jieba.cut(ques, cut_all=False, HMM=True))]).strip().replace('  ',' ')
            line_y = extract_chinese(label)
            x_y.append(line_y+','+line_x+'\n')
    return x_y


def save_json(jsons, json_path):
    """
      保存json，
    :param json_: json 
    :param path: str
    :return: None
    """
    with open(json_path, 'w', encoding='utf-8') as fj:
        fj.write(json.dumps(jsons, ensure_ascii=False))
    fj.close()


def load_json(path):
    """
      获取json，只取第一行
    :param path: str
    :return: json
    """
    with open(path, 'r', encoding='utf-8') as fj:
        model_json = json.loads(fj.readlines()[0])
    return model_json


def delete_file(path):
    """
        删除一个目录下的所有文件
    :param path: str, dir path
    :return: None
    """
    for i in os.listdir(path):
        # 取文件或者目录的绝对路径
        path_children = os.path.join(path, i)
        if os.path.isfile(path_children):
            if path_children.endswith(".h5") or path_children.endswith(".json"):
                os.remove(path_children)
        else:# 递归, 删除目录下的所有文件
            delete_file(path_children)


def get_ngram(text, ns=[1]):
    """
        获取文本的ngram等特征
    :param text: str
    :return: list
    """
    if type(ns) != list:
        raise RuntimeError("ns of function get_ngram() must be list!")
    for n in ns:
        if n < 1:
            raise RuntimeError("enum of ns must '>1'!")
    len_text = len(text)
    ngrams = []
    for n in ns:
        ngram_n = []
        for i in range(len_text):
            if i + n <= len_text:
                ngram_n.append(text[i:i+n])
            else:
                break
        if not ngram_n:
            ngram_n.append(text)
        ngrams += ngram_n
    return ngrams


def transform_multilabel_to_multihot(sample, label=1070):
    """

    :param sample: [1, 2, 3, 4]
    :param label: 1022
    :return: [1, 0, 1, 1, ......]
    """
    result = np.zeros(label)
    result[sample] = 1
    res = result.tolist()
    # res = ''.join([str(r) for r in res])
    return res


class PreprocessText:
    """
        数据预处理, 输入为csv格式, [label,ques]
    """
    def __init__(self, path_model_dir):
        self.l2i_i2l = None
        self.path_fast_text_model_vocab2index = path_model_dir + 'vocab2index.json'
        self.path_fast_text_model_l2i_i2l = path_model_dir + 'l2i_i2l.json'
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            self.l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

    def prereocess_idx(self, pred, digits=5):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_i2l = {}
            i2l = self.l2i_i2l['i2l']
            for i in range(len(pred)):
                pred_i2l[i2l[str(i)]] = round(float(pred[i]), digits)
            pred_i2l_rank = [sorted(pred_i2l.items(), key=lambda k: k[1], reverse=True)]
            return pred_i2l_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def prereocess_pred_xid(self, pred):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_l2i = {}
            l2i = self.l2i_i2l['l2i']
            for i in range(len(pred)):
                pred_l2i[pred[i]] = l2i[pred[i]]
            pred_l2i_rank = [sorted(pred_l2i.items(), key=lambda k: k[1], reverse=True)]
            return pred_l2i_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def preprocess_label_ques_to_idx(self, embedding_type, path, embed, rate=1, shuffle=True, graph=None):
        data = pd.read_csv(path)
        ques = data['ques'].tolist()
        label = data['label'].tolist()
        ques = [str(q).upper() for q in ques]
        label = [str(l).upper() for l in label]
        if shuffle:
            ques = np.array(ques)
            label = np.array(label)
            indexs = [ids for ids in range(len(label))]
            random.shuffle(indexs)
            ques, label = ques[indexs].tolist(), label[indexs].tolist()
        # 如果label2index存在则不转换了
        if not os.path.exists(self.path_fast_text_model_l2i_i2l):
            label_set = set(label)
            count = 0
            label2index = {}
            index2label = {}
            for label_one in label_set:
                label2index[label_one] = count
                index2label[count] = label_one
                count = count + 1

            l2i_i2l = {}
            l2i_i2l['l2i'] = label2index
            l2i_i2l['i2l'] = index2label
            save_json(l2i_i2l, self.path_fast_text_model_l2i_i2l)
        else:
            l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

        len_ql = int(rate * len(ques))
        if len_ql <= 500: # sample时候不生效,使得语料足够训练
            len_ql = len(ques)

        x = []
        print("ques to index start!")
        ques_len_ql = ques[0:len_ql]
        for i in tqdm(range(len_ql)):
            que = ques_len_ql[i]
            que_embed = embed.sentence2idx(que)
            x.append(que_embed) # [[], ]
        label_zo = []
        print("label to onehot start!")
        label_len_ql = label[0:len_ql]
        for j in tqdm(range(len_ql)):
            label_one = label_len_ql[j]
            label_zeros = [0] * len(l2i_i2l['l2i'])
            label_zeros[l2i_i2l['l2i'][label_one]] = 1
            label_zo.append(label_zeros)

        count = 0
        if embedding_type in  ['bert', 'albert']:
            x_, y_ = np.array(x), np.array(label_zo)
            x_1 = np.array([x[0] for x in x_])
            x_2 = np.array([x[1] for x in x_])
            x_all = [x_1, x_2]
            return x_all, y_
        elif embedding_type == 'xlnet':
            count += 1
            if count == 1:
                x_0 = x[0]
                print(x[0][0][0])
            x_, y_ = x, np.array(label_zo)
            x_1 = np.array([x[0][0] for x in x_])
            x_2 = np.array([x[1][0] for x in x_])
            x_3 = np.array([x[2][0] for x in x_])
            if embed.trainable:
                x_4 = np.array([x[3][0] for x in x_])
                x_all = [x_1, x_2, x_3, x_4]
            else:
                x_all = [x_1, x_2, x_3]
            return x_all, y_
        else:
            x_, y_ = np.array(x), np.array(label_zo)
            return x_, y_


class PreprocessTextMulti:
    """
        数据预处理, 输入为csv格式, [label,ques]
    """
    def __init__(self, path_model_dir):
        self.l2i_i2l = None
        self.path_fast_text_model_vocab2index = path_model_dir + 'vocab2index.json'
        self.path_fast_text_model_l2i_i2l = path_model_dir + 'l2i_i2l.json'
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            self.l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

    def prereocess_idx(self, pred, digits=5):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_i2l = {}
            i2l = self.l2i_i2l['i2l']
            for i in range(len(pred)):
                pred_i2l[i2l[str(i)]] = round(float(pred[i]), digits)
            pred_i2l_rank = [sorted(pred_i2l.items(), key=lambda k: k[1], reverse=True)]
            return pred_i2l_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def prereocess_pred_xid(self, pred):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_l2i = {}
            l2i = self.l2i_i2l['l2i']
            for i in range(len(pred)):
                pred_l2i[pred[i]] = l2i[pred[i]]
            pred_l2i_rank = [sorted(pred_l2i.items(), key=lambda k: k[1], reverse=True)]
            return pred_l2i_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def preprocess_label_ques_to_idx(self, embedding_type, path, embed, rate=1, shuffle=True):
        if type(path) == str:
            label_ques = txt_read(path)
            ques = list()
            label = list()
            for lq in label_ques[1:]:
                lqs = lq.split('|,|')
                ques.append(lqs[1])
                label.append(lqs[0])
        elif type(path) == list and ',' in path[0]:
            label = [label_ques.split(',')[0] for label_ques in path]
            ques = [label_ques.split(',')[1] for label_ques in path]
        else:
            raise RuntimeError('type of path is not true！')

        len_ql = int(rate * len(ques))
        if len_ql <= 50:  # 数量较少时候全取, 不管rate
            len_ql = len(ques)
        ques = ques[: len_ql]
        label = label[: len_ql]
        print('rate ok!')

        ques = [str(q).strip().upper() for q in ques]

        if shuffle:
            ques = np.array(ques)
            label = np.array(label)
            indexs = [ids for ids in range(len(label))]
            random.shuffle(indexs)
            ques, label = ques[indexs].tolist(), label[indexs].tolist()

        if not os.path.exists(self.path_fast_text_model_l2i_i2l):
            from keras_textclassification.conf.path_config import path_byte_multi_news_label
            byte_multi_news_label = txt_read(path_byte_multi_news_label)
            byte_multi_news_label = [i.strip().upper() for i in byte_multi_news_label]

            label_set = set(byte_multi_news_label)
            len_label_set = len(label_set)
            count = 0
            label2index = {}
            index2label = {}
            for label_one in label_set:
                label2index[label_one] = count
                index2label[count] = label_one
                count = count + 1

            l2i_i2l = {}
            l2i_i2l['l2i'] = label2index
            l2i_i2l['i2l'] = index2label
            save_json(l2i_i2l, self.path_fast_text_model_l2i_i2l)
        else:
            l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)
            len_label_set = len(l2i_i2l['l2i'])


        x = []
        print("ques to index start!")
        for i in tqdm(range(len_ql)):
            que = ques[i]
            que_embed = embed.sentence2idx(que)
            x.append(que_embed)  # [[], ]

        print('que_embed ok!')

        # 转化为多标签类标
        label_multi_list = []
        count = 0
        print("label to onehot start!")
        for j in tqdm(range(len_ql)):
            l = label[j]
            count += 1
            label_single = str(l).strip().upper().split(',')
            #print(count,label_single)
            label_single = [x for x in label_single if x != '']
            label_single_index = [l2i_i2l['l2i'][ls] for ls in label_single]
            label_multi = transform_multilabel_to_multihot(label_single_index, label=len_label_set)
            label_multi_list.append(label_multi)

        print('label_multi_list ok!')
        count = 0
        if embedding_type in  ['bert', 'albert']:
            x_, y_ = np.array(x), np.array(label_multi_list)
            x_1 = np.array([x[0] for x in x_])
            x_2 = np.array([x[1] for x in x_])
            x_all = [x_1, x_2]
            return x_all, y_
        elif embedding_type == 'xlnet':
            count += 1
            if count == 1:
                x_0 = x[0]
                print(x[0][0][0])
            x_, y_ = x, np.array(label_multi_list)
            x_1 = np.array([x[0][0] for x in x_])
            x_2 = np.array([x[1][0] for x in x_])
            x_3 = np.array([x[2][0] for x in x_])
            x_all = [x_1, x_2, x_3]
            return x_all, y_
        else:
            x_, y_ = np.array(x), np.array(label_multi_list)
            return x_, y_


class PreprocessSim:
    """
        数据预处理, 输入为csv格式, [label,ques]
    """
    def __init__(self, path_model_dir):
        self.l2i_i2l = None
        self.path_fast_text_model_vocab2index = path_model_dir + 'vocab2index.json'
        self.path_fast_text_model_l2i_i2l = path_model_dir + 'l2i_i2l.json'
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            self.l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

    def prereocess_idx(self, pred, digits=5):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_i2l = {}
            i2l = self.l2i_i2l['i2l']
            for i in range(len(pred)):
                pred_i2l[i2l[str(i)]] = round(float(pred[i]), digits)
            pred_i2l_rank = [sorted(pred_i2l.items(), key=lambda k: k[1], reverse=True)]
            return pred_i2l_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def prereocess_pred_xid(self, pred):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_l2i = {}
            l2i = self.l2i_i2l['l2i']
            for i in range(len(pred)):
                pred_l2i[pred[i]] = l2i[pred[i]]
            pred_l2i_rank = [sorted(pred_l2i.items(), key=lambda k: k[1], reverse=True)]
            return pred_l2i_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def preprocess_label_ques_to_idx(self, embedding_type, path, embed, rate=1, shuffle=True):
        data = pd.read_csv(path)
        print (data)
        print (data['sentence1'])
        ques_1 = data['sentence1'].tolist()
        ques_2 = data['sentence2'].tolist()
        label = data['label'].tolist()
        ques_1 = [str(q1).upper() for q1 in ques_1]
        ques_2 = [str(q2).upper() for q2 in ques_2]

        label = [str(l).upper() for l in label]
        if shuffle:
            ques_1 = np.array(ques_1)
            ques_2 = np.array(ques_2)
            label = np.array(label)
            indexs = [ids for ids in range(len(label))]
            random.shuffle(indexs)
            ques_1, ques_2, label = ques_1[indexs].tolist(), ques_2[indexs].tolist(), label[indexs].tolist()
        # 如果label2index存在则不转换了
        if not os.path.exists(self.path_fast_text_model_l2i_i2l):
            label_set = set(label)
            count = 0
            label2index = {}
            index2label = {}
            for label_one in label_set:
                label2index[label_one] = count
                index2label[count] = label_one
                count = count + 1

            l2i_i2l = {}
            l2i_i2l['l2i'] = label2index
            l2i_i2l['i2l'] = index2label
            save_json(l2i_i2l, self.path_fast_text_model_l2i_i2l)
        else:
            l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

        len_ql = int(rate * len(label))
        if len_ql <= 500: # sample时候不生效,使得语料足够训练
            len_ql = len(label)

        x = []
        print("ques to index start!")
        for i in tqdm(range(len_ql)):
            que_1 = ques_1[i]
            que_2 = ques_2[i]
            que_embed = embed.sentence2idx(text=que_1, second_text=que_2)
            x.append(que_embed) # [[], ]
        label_zo = []
        print("label to onehot start!")
        label_len_ql = label[0:len_ql]
        for j in tqdm(range(len_ql)):
            label_one = label_len_ql[j]
            label_zeros = [0] * len(l2i_i2l['l2i'])
            label_zeros[l2i_i2l['l2i'][label_one]] = 1
            label_zo.append(label_zeros)

        if embedding_type in  ['bert', 'albert']:
            x_, y_ = np.array(x), np.array(label_zo)
            x_1 = np.array([x[0] for x in x_])
            x_2 = np.array([x[1] for x in x_])
            x_all = [x_1, x_2]
            return x_all, y_


class PreprocessSimCCKS2020baidu:
    """
        数据预处理, 输入为csv格式, [label,ques]
    """
    def __init__(self, path_model_dir):
        self.l2i_i2l = None
        self.path_fast_text_model_vocab2index = path_model_dir + 'vocab2index.json'
        self.path_fast_text_model_l2i_i2l = path_model_dir + 'l2i_i2l.json'
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            self.l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

    def prereocess_idx(self, pred):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_i2l = {}
            i2l = self.l2i_i2l['i2l']
            for i in range(len(pred)):
                pred_i2l[i2l[str(i)]] = pred[i]
            pred_i2l_rank = [sorted(pred_i2l.items(), key=lambda k: k[1], reverse=True)]
            return pred_i2l_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def prereocess_pred_xid(self, pred):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_l2i = {}
            l2i = self.l2i_i2l['l2i']
            for i in range(len(pred)):
                pred_l2i[pred[i]] = l2i[pred[i]]
            pred_l2i_rank = [sorted(pred_l2i.items(), key=lambda k: k[1], reverse=True)]
            return pred_l2i_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def preprocess_label_ques_to_idx(self, embedding_type, path, embed,
                                     rate=1, shuffle=True, graph=None):
        if "json" in path:
            datas = txt_read(path)
            ques_1 = []
            ques_2 = []
            label = []
            offset = []
            mention = []
            for data_str in datas:
                data = json.loads(data_str)
                ques_1 += [data['sentence1']]
                ques_2 += [data['sentence2']]
                mention += [data['mention']]
                label += [data['label']]
                offset += [data['offset']]
        elif "csv" in path:
            data = pd.read_csv(path)
            ques_1 = data['sentence1'].tolist()
            ques_2 = data['sentence2'].tolist()
            label = data['label'].tolist()
            offset = data['offset'].tolist()

        ques_1 = [str(q1).upper() for q1 in ques_1]
        ques_2 = [str(q2).upper() for q2 in ques_2]

        # label = [str(l).upper() for l in label]
        label = [str(l) for l in label]
        if shuffle:
            ques_1 = np.array(ques_1)
            ques_2 = np.array(ques_2)
            label = np.array(label)
            mention = np.array(mention)
            offset = np.array(offset)

            indexs = [ids for ids in range(len(label))]
            random.shuffle(indexs)
            ques_1 = ques_1[indexs].tolist()
            ques_2 = ques_2[indexs].tolist()
            label = label[indexs].tolist()
            mention = mention[indexs].tolist()
            offset = offset[indexs].tolist()
        # 如果label2index存在则不转换了
        if not os.path.exists(self.path_fast_text_model_l2i_i2l):
            label_set = set(label)
            count = 0
            label2index = {}
            index2label = {}
            for label_one in label_set:
                label2index[label_one] = count
                index2label[count] = label_one
                count = count + 1

            l2i_i2l = {}
            l2i_i2l['l2i'] = label2index
            l2i_i2l['i2l'] = index2label
            save_json(l2i_i2l, self.path_fast_text_model_l2i_i2l)
        else:
            l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

        len_ql = int(rate * len(label))
        if len_ql <= 1: # sample时候不生效,使得语料足够训练
            len_ql = len(label)

        x = []
        print("ques to index start!")
        for i in tqdm(range(len_ql)):
            que_1 = ques_1[i]
            que_2 = ques_2[i]
            mention_1 = mention[i]
            # que_embed = embed.sentence2idx(text=que_1, second_text=que_2)
            # x.append(que_embed)  # [[], ]
            offset_i = int(offset[i])
            # ques_entity = que_1 + "##" + que_1[offset_i+len(que_2):]
            # ques_entity = que_1
            # que_embed1 = embed.sentence2idx(text=que_1, second_text=que_2)
            if embedding_type in ['bert', 'albert']:
                ########################################1111111##############
                # [input_id, input_type_id] = que_embed
                # input_entity_mask = [0] * len(input_id)
                # input_entity_mask[offset_i:offset_i+len(que_2)] = [1] * len(que_2)
                # # x.append(que_embed)  # [[], ]
                # x.append([input_id, input_type_id, input_entity_mask])
                # # x.append([input_id, input_type_id, input_entity_mask, offset_i])
                ########################################2222222指针网络######################################
                # [input_id, input_type_id] = que_embed
                # input_start_mask = [0] * len(input_id)
                # input_start_mask[offset_i] = 1
                # input_end_mask = [0] * len(input_id)
                # input_end_mask[offset_i + len(mention_1) - 1] = 1
                # x.append([input_id, input_type_id, input_start_mask, input_start_mask])
                ########################################分开两个句子###################################################
                que_embed_1 = embed.sentence2idx(text=que_1)
                # que_embed_1 = [que[:54] for que in que_embed_1]

                que_embed_2 = embed.sentence2idx(text=que_2)
                # que_embed_2 = [que[:256-54] for que in que_embed_2]
                try:
                    """ques1"""
                    [input_id_1, input_type_id_1, input_mask_1] = que_embed_1
                    input_start_mask_1 = [0] * len(input_id_1)
                    input_start_mask_1[offset_i] = 1
                    input_end_mask_1 = [0] * len(input_id_1)
                    input_end_mask_1[offset_i+len(mention_1)-1] = 1
                    input_entity_mask_1 = [0] * len(input_id_1)
                    input_entity_mask_1[offset_i:offset_i+len(mention_1)] = [1] * len(mention_1)
                    """ques2"""
                    [input_id_2, input_type_id_2, input_mask_2] = que_embed_2
                    kind_2 = [0] * len(input_type_id_2)
                    que_2_sp = que_2.split("|")
                    que_2_sp_sp = que_2_sp[0].split(":")
                    kind_2_start = len(que_2_sp_sp[0]) - 1
                    kind_2_end = kind_2_start + len(que_2_sp_sp[1]) - 1
                    kind_2[kind_2_start:kind_2_end] = [1] * (kind_2_end-kind_2_start)
                    kind_21 = [0] * len(input_type_id_2)
                    if "标签" in que_2_sp[1]:
                        que_21_sp_sp = que_2_sp[1].split(":")
                        kind_21_start = len(que_2_sp[0]) + len(que_21_sp_sp[0]) - 1
                        kind_21_end = len(que_2_sp[0]) + len(que_21_sp_sp[0]) + len(que_21_sp_sp[1]) - 1
                        kind_21[kind_21_start:kind_21_end] = [1] * (kind_21_end - kind_21_start)
                except Exception as e:
                    print(str(e))
                    gg = 0

                x.append([input_id_1, input_type_id_1, input_mask_1, input_start_mask_1, input_end_mask_1, input_entity_mask_1,
                          input_id_2, input_type_id_2, input_mask_2, kind_2, kind_21])


            elif embedding_type == 'xlnet':
                if embed.trainable:
                    [token_input, segment_input, memory_length_input, mask_input] = que_embed
                    input_entity_mask = [0] * len(token_input)
                    input_entity_mask[offset_i:offset_i + len(que_2)] = [1] * len(que_2)
                    # x.append(que_embed)  # [[], ]
                    x.append([token_input, segment_input, memory_length_input, mask_input, input_entity_mask])
                else:
                    [token_input, segment_input, memory_length_input] = que_embed
                    input_entity_mask = [0] * len(token_input)
                    input_entity_mask[offset_i:offset_i + len(que_2)] = [1] * len(que_2)
                    x.append([token_input, segment_input, memory_length_input, input_entity_mask])

        label_zo = []
        print("label to onehot start!")
        label_len_ql = label[0:len_ql]
        for j in tqdm(range(len_ql)):
            label_one = label_len_ql[j]
            label_zeros = [0] * len(l2i_i2l['l2i'])
            label_zeros[l2i_i2l['l2i'][label_one]] = 1
            label_zo.append(label_zeros)

        if embedding_type in  ['bert', 'albert']:
            x_, y_ = np.array(x), np.array(label_zo)
            # x_1 = np.array([x[0] for x in x_])
            # x_2 = np.array([x[1] for x in x_])
            # x_3 = np.array([x[2] for x in x_])
            # x_4 = np.array([x[3] for x in x_])
            # x_all = [x_1, x_2, x_3, x_4]
            x_all = []
            for i in range(len(x_[0])):
                x_all.append(np.array([x[i] for x in x_]))
            return x_all, y_
        elif embedding_type == 'xlnet':
            x_, y_ = x, np.array(label_zo)
            x_1 = np.array([x[0][0] for x in x_])
            x_2 = np.array([x[1][0] for x in x_])
            x_3 = np.array([x[2][0] for x in x_])
            x_4 = np.array([x[3][0] for x in x_])
            if embed.trainable:
                x_5 = np.array([x[4][0] for x in x_])
                x_all = [x_1, x_2, x_3, x_4, x_5]
            else:
                x_all = [x_1, x_2, x_3, x_4]
            return x_all, y_
        else:
            x_, y_ = np.array(x), np.array(label_zo)
            return x_, y_


class PreprocessSimConv2019:
    """
        数据预处理, 输入为csv格式, [label,ques]
    """
    def __init__(self, path_model_dir):
        self.l2i_i2l = None
        self.path_fast_text_model_vocab2index = path_model_dir + 'vocab2index.json'
        self.path_fast_text_model_l2i_i2l = path_model_dir + 'l2i_i2l.json'
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            self.l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

    def prereocess_idx(self, pred):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_i2l = {}
            i2l = self.l2i_i2l['i2l']
            for i in range(len(pred)):
                pred_i2l[i2l[str(i)]] = pred[i]
            pred_i2l_rank = [sorted(pred_i2l.items(), key=lambda k: k[1], reverse=True)]
            return pred_i2l_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def prereocess_pred_xid(self, pred):
        if os.path.exists(self.path_fast_text_model_l2i_i2l):
            pred_l2i = {}
            l2i = self.l2i_i2l['l2i']
            for i in range(len(pred)):
                pred_l2i[pred[i]] = l2i[pred[i]]
            pred_l2i_rank = [sorted(pred_l2i.items(), key=lambda k: k[1], reverse=True)]
            return pred_l2i_rank
        else:
            raise RuntimeError("path_fast_text_model_label2index is None")

    def preprocess_label_ques_to_idx(self, embedding_type, path, embed, rate=1, shuffle=True):
        data = pd.read_csv(path)
        # category, query1, query2, label
        ques_1 = data['query1'].tolist()
        category = data['category'].tolist()
        ques_2 = data['query2'].tolist()
        label = data['label'].tolist()
        ques_1 = [str(q1).upper() for q1 in ques_1]
        ques_2 = [str(q2).upper() for q2 in ques_2]

        label = [str(l).upper() for l in label]
        if shuffle:
            ques_1 = np.array(ques_1)
            ques_2 = np.array(ques_2)
            category = np.array(category)
            label = np.array(label)
            indexs = [ids for ids in range(len(label))]
            random.shuffle(indexs)
            ques_1, ques_2, label, category = ques_1[indexs].tolist(), ques_2[indexs].tolist(), label[indexs].tolist(), category[indexs].tolist()
        # 如果label2index存在则不转换了
        if not os.path.exists(self.path_fast_text_model_l2i_i2l):
            label_set = set(label)
            count = 0
            label2index = {}
            index2label = {}
            for label_one in label_set:
                label2index[label_one] = count
                index2label[count] = label_one
                count = count + 1

            l2i_i2l = {}
            l2i_i2l['l2i'] = label2index
            l2i_i2l['i2l'] = index2label
            save_json(l2i_i2l, self.path_fast_text_model_l2i_i2l)
        else:
            l2i_i2l = load_json(self.path_fast_text_model_l2i_i2l)

        len_ql = int(rate * len(label))
        if len_ql <= 500: # sample时候不生效,使得语料足够训练
            len_ql = len(label)

        x = []
        print("ques to index start!")
        len_ques_list = []
        label_list = []
        for i in tqdm(range(len_ql)):
            que_1 = ques_1[i]
            que_2 = ques_2[i]
            category_3 = category[i]
            que_embed = embed.sentence2idx(text=category_3+":"+que_1, second_text=category_3+":"+que_2)

            # que_embed = embed.sentence2idx(text=category_3+":"+que_1, second_text=category_3+":"+que_2)
            # que_embed = embed.sentence2idx(text=que_1, second_text=que_2)
            x.append(que_embed) # [[], ]
            len_ques_list.append(len(que_1+que_2))
            label_list.append(category_3)
        len_ques_counter = Counter(len_ques_list)
        label_counter = Counter(label_list)
        print("长度:{}".format(dict(len_ques_counter)))
        print("长度字典:{}".format(dict(len_ques_counter).keys()))
        print("最大长度:{}".format(max(list(dict(len_ques_counter).keys()))))
        print("类别字典:{}".format(dict(label_counter)))
        label_zo = []
        print("label to onehot start!")
        label_len_ql = label[0:len_ql]
        for j in tqdm(range(len_ql)):
            label_one = label_len_ql[j]
            label_zeros = [0] * len(l2i_i2l['l2i'])
            label_zeros[l2i_i2l['l2i'][label_one]] = 1
            label_zo.append(label_zeros)

        if embedding_type in  ['bert', 'albert']:
            x_, y_ = np.array(x), np.array(label_zo)
            x_1 = np.array([x[0] for x in x_])
            x_2 = np.array([x[1] for x in x_])
            x_all = [x_1, x_2]
            return x_all, y_
        else:
            x_, y_ = np.array(x), np.array(label_zo)

            return x_, y_

