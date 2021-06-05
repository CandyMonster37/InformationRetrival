# -*- coding: utf-8 -*-
import os
from utils.IO_contral import readfiles
from utils.vb_compression import vb_decode, vb_encode, print_vb_code
import time
import nltk
from utils.SBSTree import sbst
import re
import jieba
import math
from collections import Counter
import operator

# import numpy as np

punctuations = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
                '{', '}', '|', '<', '>', '?', ':', '"', '"', ',', '.', '/',
                ';', "'", "'", '[', ']', '-', '=', '`', '·', '！', '@', '#',
                '￥', '%', '…', '…', '&', '*', '（', '）', '—', '—', '-', '{',
                '}', '|', '、', '【', '】', '：', '“', '”', '；', '‘', '’', '《',
                '》', '？', '，', '。', '\n', '\\', ' ']


class StaticObjects:
    def __init__(self):
        self.documents = ''
        self.document_words = ''
        self.indextable = ''
        self.doc_lists = []


class CompressTable:

    def __init__(self, compress_doc_id, compress_doc_fre, compress_word):
        self.compress_doc_id = compress_doc_id
        self.compress_doc_fre = compress_doc_fre
        self.compress_word = compress_word

    def keys(self):
        return self.compress_word

    def get(self, word, default=None):
        for i in range(len(self.compress_word)):
            if self.compress_word[i] == word:
                # 解码
                docIDs = vb_decode(self.compress_doc_id[i])
                docFres = vb_decode(self.compress_doc_fre[i])
                # 求ID
                for j in range(1, len(docIDs)):
                    docIDs[j] = docIDs[j] - docIDs[j - 1]
                tep_list = []
                dic = {}
                for j in range(len(docIDs)):
                    dic[docIDs[j]] = docFres[j]
                tep_list.append(dic)
                tep_list.append(len(dic))
                return tep_list
        return default

    def __getitem__(self, word, default=None):
        for i in range(len(self.compress_word)):
            if self.compress_word[i] == word:
                # 解码
                docIDs = vb_decode(self.compress_doc_id[i])
                docFres = vb_decode(self.compress_doc_fre[i])
                # 求ID
                for j in range(1, len(docIDs)):
                    docIDs[j] = docIDs[j] - docIDs[j - 1]
                tep_list = []
                dic = {}
                for j in range(len(docIDs)):
                    dic[docIDs[j]] = docFres[j]
                tep_list.append(dic)
                tep_list.append(len(dic))
                return tep_list


class IndexTable:
    def __init__(self, document_words):
        self.tep_table = {}
        self.table = None
        self.tep_table_2 = {}
        self.table_2 = None
        self.document_words = document_words
        self.permuterm_index_table = False
        self.length = 0
        self.length_2 = 0

    def insert_pair(self, word, docID):
        IDlist = self.tep_table.get(word, 'null')
        if IDlist != 'null':
            if IDlist[0].get(docID, 'null') != 'null':
                IDlist[0][docID] += 1
            else:
                IDlist[0][docID] = 1
                IDlist[1] += 1
        else:
            self.tep_table[word] = [{docID: 1}, 1]
            self.length += 1

    def insert_pair_2(self, word, docID):
        IDlist = self.tep_table_2.get(word, 'null')
        if IDlist != 'null':
            if IDlist.get(docID, 'null') != 'null':
                IDlist[docID] += 1
            else:
                IDlist[docID] = 1
        else:
            self.tep_table_2[word] = {docID: 1}
            self.length_2 += 1

    def get_docIDs(self, word):
        IDlist = self.table.get(word, 'null')
        if IDlist == 'null':
            return []
        else:
            return IDlist[0].keys()

    def create_Permuterm_index(self):
        print('Begin creating Permuterm index.')
        t = time.time()
        self.permuterm_index_table = sbst()
        for item in self.table.keys():
            word = item + '$'
            for i in range(len(word)):
                self.permuterm_index_table.add([word[i:] + word[:i], item])
        print('Finished creating Permuterm index. Elasped time: ', time.time() - t, 's')

    # 索引压缩(VB编码)
    def index_compression(self):
        words = list(self.tep_table)
        docIDs = []
        docFres = []
        compress_word = []
        compress_doc_id = []
        compress_doc_fre = []
        for word in words:
            docIDs.append(list(self.tep_table[word][0]))
        for i in range(len(docIDs)):
            temp = []
            docIDs[i].sort()
            for j in range(len(docIDs[i])):
                temp.append(self.tep_table[words[i]][0][docIDs[i][j]])
            docFres.append(temp)
        for i in range(len(docIDs)):  # 求间距
            for j in range(1, len(docIDs[i])):
                docIDs[i][len(docIDs[i]) - j] = docIDs[i][len(docIDs[i]) - j] + docIDs[i][len(docIDs[i]) - j - 1]
        for i in range(len(docIDs)):  # 编码
            compress_doc_id.append(vb_encode(docIDs[i]))
            compress_doc_fre.append(vb_encode(docFres[i]))
        compress_word = words
        self.tep_table = {}
        self.table = CompressTable(compress_doc_id, compress_doc_fre, compress_word)
        # 如果有table_2
        words = list(self.tep_table_2)
        docIDs = []
        docFres = []
        compress_word = []
        compress_doc_id = []
        compress_doc_fre = []
        for word in words:
            docIDs.append(list(self.tep_table_2[word]))
        for i in range(len(docIDs)):
            temp = []
            docIDs[i].sort()
            for j in range(len(docIDs[i])):
                temp.append(self.tep_table_2[words[i]][docIDs[i][j]])
            docFres.append(temp)
        for i in range(len(docIDs)):  # 求间距
            for j in range(1, len(docIDs[i])):
                docIDs[i][len(docIDs[i]) - j] = docIDs[i][len(docIDs[i]) - j] + docIDs[i][len(docIDs[i]) - j - 1]
        for i in range(len(docIDs)):  # 编码
            compress_doc_id.append(vb_encode(docIDs[i]))
            compress_doc_fre.append(vb_encode(docFres[i]))
        compress_word = words
        self.tep_table_2 = {}
        self.table_2 = CompressTable(compress_doc_id, compress_doc_fre, compress_word)

    # 打印索引
    def show_index(self, word):
        for i in range(len(self.table.compress_word)):
            if self.table.compress_word[i] == word:
                print(self.table.compress_doc_id[i])
                print_vb_code(self.table.compress_doc_id[i])


def tokenize(documents, language='en'):
    document_words = {}
    if language == 'en':
        for _doc in documents.items():
            doc = []
            tar_str = _doc[1]
            words = tar_str.replace('\n', ' ').split(' ')
            for item in words:
                if item:
                    word = re.search(r'[\w]*[\d]*', item).group()
                    # 只保留单词
                    doc.append(word)
            document_words[_doc[0]] = doc
    elif language == 'zh':
        for _doc in documents.items():
            doc = []
            tar_str = _doc[1]
            cutted = jieba.cut(tar_str, cut_all=False)
            for item in cutted:
                if item in punctuations:
                    continue
                elif item:
                    doc.append(item)
            document_words[_doc[0]] = doc
    return document_words


def process(dir_name):
    t = time.time()
    print('Begin loading and build index.')
    objects = StaticObjects()
    objects.documents, objects.doc_lists = readfiles(dir_name)
    objects.document_words = tokenize(objects.documents, language='en')
    objects.indextable = IndexTable(objects.document_words)

    for words in objects.document_words.items():
        for word in words[1]:
            objects.indextable.insert_pair(word, words[0])
        for i in range(len(words[1]) - 1):
            objects.indextable.insert_pair_2(words[1][i] + ' ' + words[1][i + 1], words[0])
    # print(objects.indextable.table)
    print('Finished loading and build index. Elasped time: ', time.time() - t, 's')
    return objects
