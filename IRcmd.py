# -*- coding: utf-8 -*-
import cmd
import sys
from utils.Inverted_Index_Table import process
import operator


class IRcmder(cmd.Cmd):
    intro = "Welcome to the Information Retrival System.".center(100, ' ') + \
            "\n\nThis is a simple Information Retrival System.\n" + \
            "You can use some commands to do some work related to the information retrieval.\n" + \
            "Shell commands are defined internally.  \n\n" + \
            "Type \'help\' or \'?\' to list all available commands.\n" + \
            "Type \'help cmd\' to see more details about the command \'cmd\'.\n" + \
            "Or type \'exit\' to exit this system.\n\n"

    def __init__(self):
        super(IRcmder, self).__init__()
        self.k = 10

    def do_change_k(self, args):
        try:
            ori = self.k
            tar = int(args)
            self.k = tar
            print('Successfully change k from {0} to {1}!'.format(ori, tar))
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
        cmd_info = cmd_info + 'Later an inverted index table will be built and saved to \'/tmpdata/IndexTable.pkl\''
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


if __name__ == '__main__':
    info = "\n\nThis is a simple Information Retrival System.\nCopyright 2021 " \
           "@CandyMonster37: https://github.com/CandyMonster37\n" + \
           "A course final project for Information Retrival, and you can find the latest vertion of the codes " \
           "here: \n   https://github.com/CandyMonster37/InformationRetrival.git \n\n\n"

    print(info)

    IRcmder.prompt = 'IR > '
    IRcmder().cmdloop()
