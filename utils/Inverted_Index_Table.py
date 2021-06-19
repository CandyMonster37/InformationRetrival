# -*- coding: utf-8 -*-
import os
from utils.IO_contral import readfiles, show_summary
from utils.vb_compression import vb_decode, vb_encode, print_vb_code
from utils.SBSTree import sbst
from utils.boolean import vector_encode, vector_decode, boolean_op
import re
import jieba
import math
from collections import Counter
import operator
import numpy as np

# import numpy as np

punctuations = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
                '{', '}', '|', '<', '>', '?', ':', '"', '"', ',', '.', '/',
                ';', "'", "'", '[', ']', '-', '=', '`', '·', '！', '@', '#',
                '￥', '%', '…', '…', '&', '*', '（', '）', '—', '—', '-', '{',
                '}', '|', '、', '【', '】', '：', '“', '”', '；', '‘', '’', '《',
                '》', '？', '，', '。', '\n', '\\', ' ']


class StaticObjects:
    def __init__(self):
        self.documents = None
        self.document_words = None
        self.indextable = None
        self.doc_lists = None


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

    def get_docIDs_with_TF(self, word):
        IDlist = self.table.get(word, 'null')
        if IDlist == 'null':
            return []
        else:
            return IDlist[0]

    def get_IDF(self, word):
        IDlist = self.table.get(word, 'null')
        if IDlist == 'null':
            return 0
        else:
            return IDlist[1]

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
        print('\n')

    # 创建轮排表
    def create_Permuterm_index(self):
        print('Begin creating Permuterm index.')
        self.permuterm_index_table = sbst()
        for item in self.table.keys():
            word = item + '$'
            for i in range(len(word)):
                self.permuterm_index_table.add([word[i:] + word[:i], item])
        print('Finished creating Permuterm index. \n')

    # 查找正则词
    def find_regex_words(self, _prefix):
        prefix = _prefix + '$'
        prefix = prefix[prefix.rindex('*') + 1:] + prefix[:prefix.index('*')]
        candidates = []
        for i in self.permuterm_index_table.forward_from(prefix):
            if not i[0].startswith(prefix):
                break
            candidates.append(i)
        prefix = _prefix.split('*')
        candidates_filterd = []
        for _candidate in candidates:
            seed = False
            candidate = _candidate[1]
            for pre in prefix:
                try:
                    candidate = candidate[candidate.index(pre) + len(pre):]
                except:
                    seed = True
                    break
            if not seed:
                candidates_filterd.append(_candidate[1])

        return candidates_filterd

    # 计算TF-IDF，暂不支持中文
    def compute_TFIDF(self, sentence_, language='en'):
        sentence = []
        if language == 'en':
            words = sentence_.split(' ')
            for item in words:
                if item:
                    sentence.append(item)
        elif language == 'zh':
            pass
        else:
            print("no support language")
            raise
        scores = {}
        sentence = Counter(sentence)
        for piece in sentence.items():
            doc_list = self.table[piece[0]]
            weight = (1 + math.log10(piece[1])) * math.log10(self.length / doc_list[1])
            for doc in doc_list[0].items():
                if scores.get(doc[0], 'null') != 'null':
                    scores[doc[0]] += (1 + math.log10(doc[1])) * math.log10(self.length / doc_list[1]) * weight
                else:
                    scores[doc[0]] = (1 + math.log10(doc[1])) * math.log10(self.length / doc_list[1]) * weight
        for i in scores.items():
            scores[i[0]] = scores[i[0]] / len(self.document_words[i[0]])
        scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        return scores

    # 布尔查询 暂不支持中文
    def boolean_query(self, words, doc_list):
        priority = {'AND': 1, 'OR': 1, 'NOT': 2, '(': 0}
        stack = []  # 只存单词不存操作
        op = []  # 只存操作不存单词
        ret = []
        for i in range(0, len(words)):
            if words[i] == 'AND' or words[i] == 'OR' or words[i] == 'NOT':
                while (len(op) > 0) and priority[op[len(op) - 1]] >= priority[words[i]]:
                    stack = boolean_op(op.pop(), stack)
                op.append(words[i])
            elif words[i] == '(':
                op.append('(')
            elif words[i] == ')':
                while len(op) > 0 and op[len(op) - 1] != '(':
                    stack = boolean_op(op.pop(), stack)
                op.pop()
            else:
                # 普通单词送stack
                vec = vector_encode(self.table.get(words[i], [{}, 0])[0], doc_list)
                stack.append(vec)

        while len(op) > 0:
            stack = boolean_op(op.pop(), stack)
        if len(stack) > 1:
            return 'Invalid boolean expression.'
        res = stack[0]
        ret = vector_decode(res, doc_list)
        return ret

    # 词推荐
    def correction(self, word):
        print('correcting...')
        candidates = []
        for key in self.table.keys():
            if abs(len(word) - len(key)) < 3 and Levenshtein_Distance(word, key) < 3:
                candidates.append(key)
        if len(candidates):
            print('\nYou may want to search:')
            print(' '.join(candidates) + '\n\n')

    #  短语查询 暂不支持中文
    def phrase_query(self, args, language='en'):
        sentence = []
        if language == 'en':
            words = args.split(' ')
            for item in words:
                if item:
                    sentence.append(item)
        elif language == 'zh':
            pass
        else:
            print("no support language")
            raise
        docs = []
        for i in range(len(sentence)-1):
            ret = self.table_2.get(sentence[i] + ' ' + sentence[i + 1], 'none')
            if ret == 'none':
                return []
            docs.append(set(ret[0].keys()))
        docs = set.intersection(*docs)
        docs_filterd = []
        for doc in docs:
            for i in range(len(self.document_words[doc])):
                seed = False
                if i == sentence[0]:
                    for index, token in enumerate(sentence):
                        if token != self.document_words[doc][i + index]:
                            seed = True
                            break
                if seed == False:
                    docs_filterd.append(doc)

        return docs_filterd

    # 只计算指定文档的TF-IDF，暂不支持中文
    def compute_TFIDF_with_docID(self, sentence_, docID, language='en'):
        sentence = []
        if language == 'en':
            words = sentence_.split(' ')
            for item in words:
                if item:
                    sentence.append(item)
        elif language == 'zh':
            pass
        else:
            print("no support language")
            raise
        score = 0
        sentence = Counter(sentence)
        for piece in sentence.items():
            doc_list = self.table[piece[0]]
            weight = (1 + math.log10(piece[1])) * math.log10(self.length / doc_list[1])
            ret = doc_list[0].get(docID, 'none')
            if ret != 'none':
                score += (1 + math.log10(ret)) * math.log10(self.length / doc_list[1]) * weight
            score = score / len(self.document_words[docID])
        return score


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
        return document_words
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
    else:
        print("no support language")
        raise


def process(args):
    pre_mattched = args.split(' ')  # do re
    rule = r'(?<=language=)[\w]*'
    lan = ''
    for item in pre_mattched:
        res = re.search(rule, item)
        if res:
            lan = res.group()
            pre_mattched.remove(item)
            break
    if not lan:
        lan = 'en'
    dir_name = pre_mattched[0]

    print('Begin loading and build index.')
    objects = StaticObjects()
    objects.documents, objects.doc_lists = readfiles(dir_name)
    objects.document_words = tokenize(objects.documents, language=lan)
    objects.indextable = IndexTable(objects.document_words)

    for words in objects.document_words.items():
        for word in words[1]:
            objects.indextable.insert_pair(word, words[0])
        for i in range(len(words[1]) - 1):
            objects.indextable.insert_pair_2(words[1][i] + ' ' + words[1][i + 1], words[0])
    # print(objects.indextable.table)
    print('Finished loading and build index.\n')

    return objects


# 编辑距离
def Levenshtein_Distance(str1, str2):
    m = len(str1)
    n = len(str2)
    M = np.zeros((m + 1, n + 1))
    flag = 0
    for i in range(m + 1):
        M[i][0] = i
    for j in range(n + 1):
        M[0][j] = j
    for i in range(1, m + 1):
        flag = 1
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                M[i][j] = min(M[i - 1][j] + 1, M[i][j - 1] + 1, M[i - 1][j - 1])
            else:
                M[i][j] = min(M[i - 1][j] + 1, M[i][j - 1] + 1, M[i - 1][j - 1] + 1)
            if M[i][j] < 3:
                flag = 0
        if flag == 1:
            return 10
    return int(M[m][n])
