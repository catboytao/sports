#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 19/03/2020 19:59
# @Author  : Alan
# @Site    : 
# @File    : model.py
# @Software: PyCharm
import json
from collections import OrderedDict
from datetime import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from utils.core import db



class Sports(db.Model):

    __tablename__ = 'sports'
    id = db.Column(db.Integer,primary_key=True)
    start_time = db.Column(db.DateTime)
    categroy = db.Column(db.Text)
    project = db.Column(db.Text)
    contest = db.Column(db.Text)
    link = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.now)

    @staticmethod
    def user_to_dict(sport):
        return OrderedDict(
            id=sport.id,
            start_time=str(sport.start_time),
            categroy=sport.categroy,
            project=sport.project,
            contest = sport.contest,
            link = sport.link,
        )

from passlib.apps import custom_app_context as pwd_context

class User(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(32),index=True)
    password_hash = db.Column(db.String(500))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, app,expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token,app):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

class Yuanyou(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date_1 = db.Column(db.VARCHAR(20))
    data_name = db.Column(db.Text)
    before = db.Column(db.VARCHAR(20))
    forecast = db.Column(db.VARCHAR(20))
    publish = db.Column(db.VARCHAR(20))
    affect = db.Column(db.VARCHAR(10))
    create_time = db.Column(db.DateTime, default=datetime.now)


