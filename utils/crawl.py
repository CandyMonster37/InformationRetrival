# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup as bs
import random
import time
import math
import os
import re
from utils.IO_contral import save_novel

ua_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 "
    "OPR/26.0.1656.60",
    "Opera/8.0 (Windows NT 5.1; U; en)",
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 "
    "Safari/534.16",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 "
    "Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 "
    "TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 "
    "LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
    "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR "
    "3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X "
    "MetaSr 1.0",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE "
    "2.X MetaSr 1.0)",
]


def get_html(url, show=True):
    headers = {'Connection': 'close', 'User-Agent': random.choice(ua_list)}

    try:
        res = requests.get(url, headers=headers)
        if show:
            print('url:', url)
            print('get response successfully! ', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # print(res.status_code)
        res.encoding = res.apparent_encoding
        html = res.text
        return html
    except requests.HTTPError as e:
        print('http error: status_code', e)
        return ""
    except Exception as e:
        print('other error:')
        print(e)
        return ""


class Spider:
    def __init__(self, limit=30, save_dir='./data'):
        self.limit = limit
        self.base_url = 'http://novel.tingroom.com'
        self.novel_url_dic = {}
        self.t_start = None
        self.t_end = None
        self.nums = 0
        self.save_dir = save_dir

    def get_novels(self, wait=None):
        self.t_start = time.time()
        piece = 10
        pages = math.ceil(self.limit / piece)
        for i in range(pages):
            if len(self.novel_url_dic) >= self.limit:
                break
            rela_add = '/duanpian/list_31_{0}.html'.format(i + 1)
            tar = self.base_url + rela_add
            html_page = get_html(url=tar, show=True)
            if not html_page:
                continue
            soup = bs(html_page, 'html.parser')
            novels_url_path = 'body > div.zhongvb > div.zhongz > div > div > div.all001xp1 > div > div.text > h6 > a'
            novels_url = soup.select(novels_url_path)
            for item in novels_url:
                novel = self.base_url + item.get('href')
                novel_name = item.text
                if novel not in self.novel_url_dic:
                    self.novel_url_dic[novel_name] = novel
                if len(self.novel_url_dic) >= self.limit:
                    break
            if wait:
                time.sleep(wait)

    def get_chapter(self, wait=None):
        for item in self.novel_url_dic.keys():
            # item：一个小说的名字，value是url
            print(item)
            html_chapter = get_html(url=self.novel_url_dic[item], show=True)
            if not html_chapter:
                continue
            soup = bs(html_chapter, 'html.parser')
            chapters_url_path = '#book_detail > ol > li > a'
            chapters_url = soup.select(chapters_url_path)  # 章节列表

            for each in chapters_url:
                chapter = self.novel_url_dic[item] + '/' + each.get('href')
                # chapter：小说的某一章的文本
                html_essay = get_html(url=chapter, show=True)
                if not html_essay:
                    continue
                soup_essay = bs(html_essay, 'html.parser')

                title_path = '#showmain > div.title > span'
                title = soup_essay.select(title_path)
                file_name = item + '-' + title[0].text + '.txt'  # 小说名+章节标题
                print(file_name)
                tar_file = os.path.join(self.save_dir, file_name)

                cont_path = '#tt_text > div'
                cont = soup_essay.select(cont_path)
                rule1 = r'该作者的'
                rule2 = r'点击收听'
                essay = []
                for part in cont:
                    con = part.text.strip().strip('\n')
                    if not con:
                        continue
                    res = re.search(rule1, con)
                    if res:
                        break
                    res = re.search(rule2, con)
                    if res:
                        break
                    essay.append(con)
                essay = '\n'.join(essay)  # 小说主体
                save_novel(cont=essay, file=tar_file)
                self.nums += 1
                if wait:
                    time.sleep(wait)
        self.t_end = time.time()
        print('\n'*80)
        print('Successfully get {0} essays!(in {1:.5f} seconds)\n'.format(self.nums, self.t_end - self.t_start))


if __name__ == '__main__':
    bug = Spider(10)
    bug.get_novels()
    bug.get_chapter()
