#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 19/03/2020 15:46
# @Author  : Alan
# @Site    : 
# @File    : crawler.py
# @Software: PyCharm
from datetime import datetime

from lxml import etree

import requests

#from load_data import Loader

headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
    "cookie":"UM_distinctid=170f1b5c5c333a-02cfe1783167e6-4313f6a-144000-170f1b5c5c49d2; CNZZDATA4622981=cnzz_eid%3D2010298943-1584603128-%26ntime%3D1584603128",
}

class Crawler(object):
    @staticmethod
    def get_html():
        url = "https://www.ballbar.cc/api/list_html.php"
        rep = requests.get(url,headers=headers)
        status = rep.status_code
        if status == 200:
            return rep.text
    @staticmethod
    def parse_html(text):
        all_data = []
        doc = etree.HTML(text)
        #print(doc)
        rows = doc.xpath('//table//tr')
        for index,row in enumerate(rows):
            if index == 0 or index == 1:
                continue
            ths = row.xpath("th")
            data = dict()
            names = ['start_time','categroy','project','contest','id','link']
            for j,th in enumerate(ths):

                if j == len(ths) - 1:
                    href = th.xpath("a/@href")
                    if href:
                        content = href[0]
                    else:
                        content = ''

                elif j == 0:
                    time_str = th.xpath("text()")[0]
                    #print(time_str)
                    content = datetime.strptime(time_str,'%Y-%m-%d %H:%M')

                else:
                    content = th.xpath("text()")[0]

                data[names[j]] = content

            if data['categroy'] == "篮球" or data['categroy'] == "足球":
                all_data.append(data)

        return all_data
            #print(data)
        # for index,row in enumerate(rows):
        #     #print(row)
        #     if index == 1:
        #         continue
        #     tds = row.xpath('//th/text()')
        #     print(tds)



if __name__ == '__main__':

    res = Crawler.get_html()
    #print(res)
    datas = Crawler.parse_html(res)
    print(datas)
    # loader = Loader()
    # for data in datas:
    #     loader.insert_data((
    #         data[4],
    #         data[0],
    #         data[1],
    #         data[2],
    #         data[3],
    #         data[5],
    #     ))


