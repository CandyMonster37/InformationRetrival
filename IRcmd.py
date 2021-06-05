# -*- coding: utf-8 -*-
import cmd
import sys
from utils.Inverted_Index_Table import process
import operator


class IRcmder(cmd.Cmd):
    intro = 'Welcome to the Information Retrival System.\nType help or ? to list commands.\n'

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

    def do_help(self, args):
        cmds_info = '\nThis is a simple Information Retrival System.\n\n' \
               'Options:\n\n' \
               'Documented commands (To know how to use, type help <topic>):\n' \
               '  Command  \t\t\t\t  Description\n' \
               '\n' \
               'Undocumented commands:\n' \
               '  Command  \t\t\t\t  Description\n' \
               '   exit    \t\t     Exit this system'
        print(cmds_info)

    def do_exit(self, args):
        try:
            print('Thank you for using. Goodbye.')
            sys.exit()
        except Exception as e:
            print(e)

    def emptyline(self):
        pass

    def default(self, line):
        print('Unrecognized command.\nNo such symbol : {0}'.format(line))


if __name__ == '__main__':

    info = "A simple Information Retrival System.\n" + \
           "Copyright 2021 @CandyMonster37: https://github.com/CandyMonster37\n" + \
          "A course final project for Information Retrival, and you can find the latest vertion of the codes here: " + \
          "\n  https://github.com/CandyMonster37/InformationRetrival.git \n" + \
          "Shell commands are defined internally.  Type `help' to see this list.\n" + \
          "Type \'help cmd\' to find out more about the command \'cmd\'.\n"
    print(info)

    IRcmder.prompt = 'IR > '
    IRcmder().cmdloop()
