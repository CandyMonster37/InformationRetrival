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


def show_summary(doc_list, index, word):
    filename = doc_list[index]
    intro = 'Some summary information about document \'{}\' is shown as follows:'.format(filename)
    print(intro)
    with open(filename, 'r', encoding='utf8') as f:
        text = f.read()
    sentences = text.split('.')
    rule = word[0]
    for sentence in sentences:
        if sentence:
            res = re.search(rule, sentence)
            if res:
                print(sentence + '...')
    print('\n')


if __name__ == '__main__':
    pass
