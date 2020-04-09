#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 20/03/2020 10:43
# @Author  : Alan
# @Site    : 
# @File    : task.py
# @Software: PyCharm
from datetime import datetime

from models.model import Sports
from spider.crawler import Crawler, YuanyouCrawler
from spider.load_data import Loader
from utils.core import db


def my_job():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def db_query():
    with db.app.app_context():
        data = db.session.query(Sports).first()
        print(data)

def db_insert():
    print("向sports表中插入数据")
    with db.app.app_context():
        loader = Loader()
        html = Crawler.get_html()
        data = Crawler.parse_html(html)
        print(len(data))
        loader.insert_data(datas=data)

def yuanyou_insert():
    print("向yuanyou表中插入数据")
    with db.app.app_context():
        loader = Loader()
        crawler = YuanyouCrawler()
        text = crawler.get_html()
        data = crawler.parse_html(text)
        crawler.all_data.extend(data)
        crawler.get_api_data(434)
        datas = crawler.all_data
        loader.insert_yuanyou(datas)