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
    password_hash = db.Column(db.string(128))
    # 姓名
    name = db.Column(db.String(30))

    # 意义不明
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    # 用户状态
    confirmed = db.Column(db.Boolean, default=False)
