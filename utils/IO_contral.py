# -*- coding: utf-8 -*-
import os
import re


def readfiles(dir_name):
    documents = {}
    doc_lists = []
    for file_name in os.listdir(dir_name):
        try:
            tar = os.path.join(dir_name, file_name)
            with open(tar, 'r', encoding='utf8') as f:
                text = f.read()
                doc_lists.append(tar)
                documents[doc_lists.index(tar)] = text
        except Exception as e:
            print(e)
            print(file_name)
    return documents, doc_lists


def show_summary(doc_list, index, word, phase=False):
    flag1 = True
    flag2 = False
    filename = doc_list[index]
    with open(filename, 'r', encoding='utf8') as f:
        text = f.read()
    sentences = text.split('.')
    rule = word
    for sentence in sentences:
        if sentence:
            res = re.search(rule, sentence)
            if res:
                flag2 = True
                if flag1:
                    if phase:
                        intro = 'Some summary information about document \'{0}\' with phase \'{1}\' ' \
                                'is shown as follows:'.format(filename, word)
                    else:
                        intro = 'Some summary information about document \'{0}\' with word \'{1}\' ' \
                                'is shown as follows:'.format(filename, word)
                    print(intro)
                    flag1 = False
                if sentences.index(sentence) == 0:
                    # 是文章第一句则开头不加...
                    print(sentence + '...')
                else:
                    print('...' + sentence + '...')
    return flag2


if __name__ == '__main__':
    pass
