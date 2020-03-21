#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 19/03/2020 19:42
# @Author  : Alan
# @Site    : 
# @File    : factory.py
# @Software: PyCharm
import atexit
import os
import platform

import yaml
from flask import Flask

from celery_task import celery_app
from utils.core import db, JSONEncoder,scheduler
from flask_cors import *

def create_app(config_name,config_path=None):
    app = Flask(__name__)
    CORS(app,supports_credentials=True)
    # 读取配置文件
    if not config_path:
        pwd = os.getcwd()
        config_path = os.path.join(pwd, 'config/config.yaml')
    if not config_name:
        config_name = 'PRODUCTION'

    # 读取配置文件
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)

    celery_conf = "redis://{}:{}/{}".format(app.config['REDIS_HOST'], app.config['REDIS_PORT'], app.config['REDIS_DB'])
    celery_app.conf.update({"broker_url": celery_conf, "result_backend": celery_conf})

    # 返回json格式转换
    app.json_encoder = JSONEncoder



    db.app = app
    db.init_app(app)

    # 启动定时任务
    if app.config.get("SCHEDULER_OPEN"):
        scheduler_init(app)

    return app


def read_yaml(config_name, config_path):
    """
    config_name:需要读取的配置内容
    config_path:配置文件路径
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')



def scheduler_init(app):
    """
    保证系统只启动一次定时任务
    :param app:
    :return:
    """
    if platform.system() != 'Windows':
        fcntl = __import__("fcntl")
        f = open('scheduler.lock', 'wb')
        try:
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            scheduler.init_app(app)
            scheduler.start()
            app.logger.debug('Scheduler Started,---------------')
        except:
            pass

        def unlock():
            fcntl.flock(f, fcntl.LOCK_UN)
            f.close()

        atexit.register(unlock)
    else:
        msvcrt = __import__('msvcrt')
        f = open('scheduler.lock', 'wb')
        try:
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            scheduler.init_app(app)
            scheduler.start()
            app.logger.debug('Scheduler Started,----------------')
        except:
            pass

        def _unlock_file():
            try:
                f.seek(0)
                msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
            except:
                pass

        atexit.register(_unlock_file)