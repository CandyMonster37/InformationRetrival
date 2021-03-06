# -*- coding: utf-8 -*-
import cmd
import re
import sys
from utils.Inverted_Index_Table import process
from utils.IO_contral import show_summary
from utils.crawl import Spider
import time
import operator
import os


class IRcmder(cmd.Cmd):
    intro = "Welcome to the Information Retrival System.\n".center(100, ' ')
    intro += "\n\nThis is a simple Information Retrival System.\n"
    intro += "You can use some commands to do some work related to the information retrieval.\n"
    intro += "Only supports English.\n"
    intro += "Shell commands are defined internally.  \n\n"
    intro += "Type \'help\' or \'?\' to list all available commands.\n"
    intro += "Type \'help cmd\' to see more details about the command \'cmd\'.\n"
    intro += "Or type \'exit\' to exit this system.\n\n"

    def __init__(self):
        super(IRcmder, self).__init__()
        self.k = 10

    # 爬虫获取数据
    def do_get_data(self, args):
        # get_data ./data --numbers=10 --wait=0.5
        k = 10
        un_mattched = args.split(' ')
        hit_arg_rule = r'(?<=numbers=)[\w]*'
        for item in un_mattched:
            res = re.search(hit_arg_rule, item)
            if res:
                un_mattched.remove(item)
                k_rule = r'(?<=numbers=)[\d]*'
                k = re.search(k_rule, item).group()
                break
        args = ' '.join(un_mattched)
        try:
            tar_k = int(k)
            k = tar_k
        except Exception as e:
            print(e)
        tar_seconds = None
        un_mattched = args.split(' ')
        wait_arg_rule = r'(?<=wait=)[\w]*'
        for item in un_mattched:
            res = re.search(wait_arg_rule, item)
            if res:
                un_mattched.remove(item)
                wait_rule = r'(?<=wait=)[\d]*'
                seconds = re.search(wait_rule, item).group()
                try:
                    tar_seconds = int(seconds)
                except Exception as e:
                    print(e)
                break
        args = ' '.join(un_mattched)
        dirr = args.strip(' ')
        if not os.path.exists(dirr):
            os.mkdir(dirr)
        bug = Spider(limit=k, save_dir=dirr)
        bug.get_novels(wait=tar_seconds)
        bug.get_chapter(wait=tar_seconds)

    def change_k(self, args):
        k = self.k
        un_mattched = args.split(' ')
        hit_arg_rule = r'(?<=hits=)[\w]*'
        for item in un_mattched:
            res = re.search(hit_arg_rule, item)
            if res:
                un_mattched.remove(item)
                k_rule = r'(?<=hits=)[\d]*'
                k = re.search(k_rule, item).group()
                break
        args = ' '.join(un_mattched)
        try:
            tar = int(k)
            self.k = tar
            return args
        except Exception as e:
            print(e)

    # 构建倒排表
    def do_build_table(self, args):
        try:
            self.object = process(args)
            self.object.indextable.index_compression()
            self.object.indextable.create_Permuterm_index()

        except Exception as e:
            print(e)

    # 打印索引
    def do_show_index(self, args):
        try:
            self.object.indextable.show_index(args)
        except Exception as e:
            print(e)

    # 构建轮排索引
    def do_create_Permuterm_index(self, args):
        try:
            self.object.indextable.create_Permuterm_index()
        except Exception as e:
            print(e)

    # 通配符查询
    def do_wildcard_query(self, args):
        args = self.change_k(args)
        print('\nWildcard query.')
        print('\n')
        try:
            t1 = time.time()
            if not self.object.indextable.permuterm_index_table:
                self.object.indextable.create_Permuterm_index()
            ret = self.object.indextable.find_regex_words(args)
            words = ret
            print('searched words: ', ret)
            ret = self.object.indextable.compute_TFIDF(' '.join(ret))
            t2 = time.time()
            print('Total docs: {0} (in {1:.5f} seconds)'.format(len(ret), t2 - t1))
            print('Top-{0} rankings:\n'.format(min(self.k, len(ret))))
            printed = {}
            for word in words:
                printed[word] = []
            cnt = 0
            for index, i in enumerate(ret):
                if cnt >= self.k:
                    break
                hit_info = 'doc ID: {0} '.format(i[0]).ljust(12, ' ')
                hit_info += 'TF-IDF value: {0:.5f} '.format(i[1]).ljust(22, ' ')
                hit_info += 'doc name: {0}'.format(self.object.doc_lists[i[0]])
                print(hit_info)
                for word in words:
                    if i[0] not in printed[word]:
                        if cnt >= self.k:
                            break
                        flag = show_summary(doc_list=self.object.doc_lists, index=i[0], word=word)
                        if flag:
                            # 打印过的词对应的文章不再打印
                            print('\n')
                            printed[word].append(i[0])
                            cnt += 1
            self.k = 10
        except Exception as e:
            print(e)

    # 直接查指定词，通过TF-IDF
    # def do_search_by_TFIDF(self, args):
    #     args = self.change_k(args)
    #     try:
    #         ret = self.object.indextable.compute_TFIDF(args)
    #         print('Top-%d rankings:' % self.k)
    #         for index, i in enumerate(ret):
    #             if index > self.k:
    #                 break
    #             print(i)
    #         # build Reuters
    #         # search_by_TFIDF approximately
    #     except Exception as e:
    #         print(e)

    # 布尔查询，暂不支持显示文章摘要
    def do_boolean_query(self, args):
        args = self.change_k(args)
        print('\nBoolean query.Does not support summary display temporarily.')
        print('\n')
        try:
            t1 = time.time()
            expression = args.replace('(', ' ( ').replace(')', ' ) ').split()
            m = self.object.documents.keys()
            doc_list = sorted(self.object.documents.keys())
            ret = self.object.indextable.boolean_query(expression, doc_list)
            t2 = time.time()
            if len(ret) == 0:
                print('Not found. (in {0:.5f} seconds)'.format(t2 - t1))
                if len(expression) == 1:
                    self.object.indextable.correction(expression[0])
            else:
                if ret != 'Invalid boolean expression.':
                    print('Total docs: {0} (in {1:.5f} seconds)'.format(len(ret), t2 - t1))
                    print('Top-{0} rankings:\n'.format(min(self.k, len(ret))))
                cnt = 0
                for ID in ret:
                    if cnt >= self.k:
                        break
                    result = 'doc ID: {0} '.format(ID).ljust(12, ' ')
                    result += 'doc name: {0}'.format(self.object.doc_lists[ID])
                    print(result)
                    cnt += 1
                print('\n')
        except Exception as e:
            print(e)

    # 短语查询
    def do_phrase_query(self, args):
        args = self.change_k(args)
        print('\nPhrase query.')
        print('\n')
        try:
            t1 = time.time()
            ret = self.object.indextable.phrase_query(args)
            scores = {}
            for i in ret:
                scores[i] = self.object.indextable.compute_TFIDF_with_docID(args, i)
            scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
            t2 = time.time()
            print('Total docs: {0} (in {1:.5f} seconds)'.format(len(scores), t2 - t1))
            print('Top-{0} rankings:\n'.format(min(self.k, len(scores))))
            for index, i in enumerate(scores):
                if index > self.k:
                    break
                hit_info = 'doc ID: {0} '.format(i[0]).ljust(12, ' ')
                hit_info += 'TF-IDF value: {0:.5f} '.format(i[1]).ljust(22, ' ')
                hit_info += 'doc name: {0}'.format(self.object.doc_lists[i[0]])
                print(hit_info)
                flag = show_summary(doc_list=self.object.doc_lists, index=i[0], word=args)
                if flag:
                    print('\n')
                # print(i)
        except Exception as e:
            print(e)

    def do_exit(self, args):
        try:
            print('\nThank you for using. Goodbye.\n')
            sys.exit()
        except Exception as e:
            print(e)

    def emptyline(self):
        pass

    def default(self, line):
        print('Unrecognized command.\nNo such symbol : {0}'.format(line))

    def help_build_table(self):
        cmd_info = 'command: \tbuild_table'.center(80, ' ')
        cmd_info = cmd_info + '\nbuild_table [dir] --language'.center(30, " ") + '\n\n'
        cmd_info = cmd_info + 'Before the whole project starts,'
        cmd_info = cmd_info + 'you need to build an inverted index table via this command first.\n'
        cmd_info = cmd_info + 'The program will read the files under the path [dir],'
        cmd_info = cmd_info + ' and then create an inverted index table with using VB encoding to compress.\n'
        cmd_info = cmd_info + 'You should use the parameter \'--language=\' ' \
                              'to explicitly specify the language of the text.\n\n'
        cmd_info = cmd_info + 'For example, assume that your documentation set is stored in the \'./data\' directory.\n'
        cmd_info = cmd_info + '如果文件集为中文文档，请输入: \n\tbuild_table ./data --language=zh\n'
        cmd_info = cmd_info + 'And if the language of the documentation set is English, '
        cmd_info = cmd_info + 'please type: \n\tbuild_table ./data --language=en\n\n'
        cmd_info = cmd_info + 'Later an inverted index table will be built.'
        print(cmd_info)

    def help_show_index(self):
        cmd_info = 'command: \tshow_index'.center(80, ' ')
        cmd_info = cmd_info + '\nshow_index [word]'.center(30, " ") + '\n\n'
        cmd_info = cmd_info + 'When builting the index table, I use VB code to compress.'
        cmd_info = cmd_info + '\nAfter building the index table, '
        cmd_info = cmd_info + 'you can view the VB compression code of the word you want via this command.\n\n'
        cmd_info = cmd_info + 'For example, if you want to see the VB compression code of the word \'we\','
        cmd_info = cmd_info + ' please type: \n\nshow_index we\n\n'
        cmd_info = cmd_info + 'Later the screen will show the VB compression code of \'we\'\n'
        print(cmd_info)

    def help_get_data(self):
        cmd_info = 'command: \tget_data'.center(80, ' ')
        cmd_info = cmd_info + '\nget_data [dir] --wait --numbers'.center(30, " ") + '\n\n'
        cmd_info = cmd_info + 'If you don\'t have any English text, '
        cmd_info = cmd_info + 'then you may need to get some English text for the next work.'
        cmd_info = cmd_info + '\nYou can use your own data source, ' \
                              'or use this command to get some data automatically.\n\n'
        cmd_info = cmd_info + 'For example, if you want to get some data automatically,'
        cmd_info = cmd_info + ' please type: \n\nget_data ./data --numbers=10 --wait=0.5\n\n'
        cmd_info = cmd_info + 'Later you will get some English novels as a data source\n'
        cmd_info = cmd_info + 'Of course, in order to prevent crawlers from being banned by the website, '
        cmd_info = cmd_info + 'we use the --wait parameter to wait for a period of time after each link is obtained '
        cmd_info = cmd_info + 'to avoid putting too much pressure on the server.\n'
        print(cmd_info)

    def help_boolean_query(self):
        cmd_info = 'command: \tboolean_query'.center(80, ' ')
        cmd_info = cmd_info + '\nboolean_query [options] --hit '.center(30, " ") + '\n\n'
        cmd_info = cmd_info + 'After creating the index table, you can use this command for boolean query.\n'
        cmd_info = cmd_info + 'Available operations are AND, OR and NOT, '
        cmd_info = cmd_info + 'and you can use () to combine them arbitrarily.\n'
        cmd_info = cmd_info + 'For example, if you want to find articles '
        cmd_info = cmd_info + 'that contain \'we\' and \'are\' but not \'you\','
        cmd_info = cmd_info + ' please type: \n\nboolean_query we AND are NOT you --hits=7\n\n'
        cmd_info = cmd_info + 'Later the screen will show some articles which are found.\n'
        cmd_info = cmd_info + 'Only supports English.\n'
        print(cmd_info)

    def help_phrase_query(self):
        cmd_info = 'command: \tphrase_query'.center(80, ' ')
        cmd_info = cmd_info + '\nphrase_query [phrase] --hit '.center(30, " ") + '\n\n'
        cmd_info = cmd_info + 'After creating the index table, you can use this command for phrase query.\n'
        cmd_info = cmd_info + 'For example, If you want to find an article that contains \'how is the weather today\','
        cmd_info = cmd_info + ' please type: \n\nphrase_query how is the weather today --hits=7\n\n'
        cmd_info = cmd_info + 'Later the screen will show some articles ' \
                              'with some summary information which are found.\n'
        cmd_info = cmd_info + 'Only supports English.\n'
        print(cmd_info)

    def help_wildcard_query(self):
        cmd_info = 'command: \twildcard_query'.center(80, ' ')
        cmd_info = cmd_info + '\nwildcard_query [target] --hit '.center(30, " ") + '\n\n'
        cmd_info = cmd_info + 'After creating the index table, you can use this command for wildcard query.\n'
        cmd_info = cmd_info + 'For example, If you want to find some articles that contain words starting with\'wh\' '
        cmd_info = cmd_info + '(like \'when\' or \'where\' or \'what\' or some words else),'
        cmd_info = cmd_info + ' please type: \n\nwildcard_query wh* --hits=7\n\n'
        cmd_info = cmd_info + 'Later the screen will show some articles ' \
                              'with some summary information which are found.\n'
        cmd_info = cmd_info + 'Only supports English.\n'
        print(cmd_info)


if __name__ == '__main__':
    info = "\n\nThis is a simple Information Retrival System.\nCopyright 2021 " \
           "@CandyMonster37: https://github.com/CandyMonster37\n" + \
           "A course final project for Information Retrival, and you can find the latest vertion of the codes " \
           "here: \n   https://github.com/CandyMonster37/InformationRetrival.git \n\n\n"

    print(info)

    IRcmder.prompt = 'IR > '
    IRcmder().cmdloop()
