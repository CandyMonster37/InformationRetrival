import os
import pickle


def readfiles(dir_name):
    documents = {}
    doc_lists = []
    for file_name in os.listdir(dir_name):
        try:
            tar = os.path.join(dir_name, file_name)
            with open(tar, 'r', encoding='utf8') as f:
                text = f.read()
                doc_lists.append(file_name)
                documents[doc_lists.index(file_name)] = text
        except Exception as e:
            print(e)
            print(file_name)
    return documents, doc_lists


def savefile(filename, obj):
    try:
        with open(filename, 'wb') as f:
            pickle.dump(obj, f)
    except Exception as e:
        print(e)
        print('error when saving file: ', filename)
