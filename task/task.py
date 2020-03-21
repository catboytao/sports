#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 20/03/2020 10:43
# @Author  : Alan
# @Site    : 
# @File    : task.py
# @Software: PyCharm
from datetime import datetime

from models.model import Sports
from spider.crawler import Crawler
from spider.load_data import Loader
from utils.core import db


def my_job():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def db_query():
    with db.app.app_context():
        data = db.session.query(Sports).first()
        print(data)

def db_insert():
    with db.app.app_context():
        loader = Loader()
        html = Crawler.get_html()
        data = Crawler.parse_html(html)
        print(len(data))
        loader.insert_data(datas=data)