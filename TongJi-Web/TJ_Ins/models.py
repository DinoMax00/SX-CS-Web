# -*- coding: utf-8 -*-
# @Time : 2020/11/21 19:46
# @File : models.py
# @author : Dino
# 定义网站所需要的所有数据库类型

import os

from flask import current_app
from datetime import datetime
from TJ_Ins.extensions import db
# 使用flask——login管理需要用户模型继承这个类
from flask_login import UserMixin
# 用于对密码进行加密
from werkzeug.security import generate_password_hash, check_password_hash


# 用户
class User(db.Model, UserMixin):
    # 唯一编号
    id = db.Column(db.Integer, primary_key=True)
    # 用户名与邮箱 无重复 创建索引,提高按这两个值查询的效率
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    # 加密的用户密码
    password_hash = db.Column(db.String(128))
    # 姓名
    name = db.Column(db.String(30))

    # 意义不明
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    # 用户状态
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        # 调用父类的构造函数
        super(User, self).__init__(**kwargs)
        # self.generate_avatar() #头像生成
        # self.follow(self)
        # self.set_role()

    # user的外键
    photos = db.relationship('Photo', back_populates='author', cascade='all')

    # 密码加密储存
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码验证
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 图片
class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    filename = db.Column(db.String(64))
    filename_s = db.Column(db.String(64))
    filename_m = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)
    flag = db.Column(db.Integer, default=0)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', back_populates='photos')
    # comments = db.relationship('Comment', back_populates='photo', cascade='all')
    # collectors = db.relationship('Collect', back_populates='collected', cascade='all')
    # tags = db.relationship('Tag', secondary=tagging, back_populates='photos')
