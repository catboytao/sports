#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 19/03/2020 21:02
# @Author  : Alan
# @Site    : 
# @File    : load_data.py
# @Software: PyCharm
import traceback

from models.model import Sports, db
from spider.crawler import Crawler


class Loader():

    def __init__(self):
        id_list = Sports.query.with_entities(Sports.id).all()
        self.ids = [item[0] for item in id_list]

    def dict_to_obj(self,obj,data):
        for k in data.keys():
            setattr(obj,k,data[k])



    def insert_data(self,datas):
        for data in datas:
            try:
                sport = Sports()
                self.dict_to_obj(sport,data)
                if int(sport.id) in self.ids:
                    continue
                else:
                    db.session.add(sport)
                    db.session.commit()
            except Exception as e:
                db.session.rollback()
                err = traceback.format_exc()
                print(err)
        db.session.close()
if __name__ == '__main__':
    pass
    #loader = Loader()
    #print(loader.ids)
    # html = Crawler.get_html()
    # datas = Crawler.parse_html(html)
    # loader.insert_data(datas)