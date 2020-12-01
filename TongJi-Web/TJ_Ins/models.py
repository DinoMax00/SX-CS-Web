# -*- coding: utf-8 -*-
# @Time : 2020/11/21 19:46
# @File : models.py
# @author : Dino
# 定义网站所需要的所有数据库类型

import os

from flask import current_app
from datetime import datetime
from TJ_Ins.extensions import db
# 使用flask—login管理需要用户模型继承这个类
from flask_login import UserMixin
# 头像生成
from flask_avatars import Identicon
# 用于对密码进行加密
from werkzeug.security import generate_password_hash, check_password_hash


# 关注
class Follow(db.Model):
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following', lazy='joined')
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers', lazy='joined')


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
    # 个人主页
    website = db.Column(db.String(255))
    # 个人简介
    bio = db.Column(db.String(120))
    # 地址
    location = db.Column(db.String(50))
    # 用户注册时长
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    # 用户状态
    confirmed = db.Column(db.Boolean, default=False)
    locked = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    # 三种型号的头像
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))

    # 外键
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower',
                                lazy='dynamic', cascade='all')
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed',
                                lazy='dynamic', cascade='all')
    photos = db.relationship('Photo', back_populates='author', cascade='all')
    comments = db.relationship('Comment', back_populates='author', cascade='all')
    collections = db.relationship('Collect', back_populates='collector', cascade='all')
    notifications = db.relationship('Notification', back_populates='receiver', cascade='all')

    def __init__(self, **kwargs):
        # 调用父类的构造函数
        super(User, self).__init__(**kwargs)
        self.generate_avatar()  # 头像生成
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

    # 初始化时完成头像生成
    def generate_avatar(self):
        # avatars提供的本地头像类型 像素风格
        avatar = Identicon()
        # 默认生成三张 text为随机文本
        filename = avatar.generate(text=self.username)
        self.avatar_s = filename[0]
        self.avatar_m = filename[1]
        self.avatar_l = filename[2]
        db.session.commit()

    @property
    def is_active(self):
        return self.active


tagging = db.Table('tagging',
                   db.Column('photo_id', db.Integer, db.ForeignKey('photo.id')),
                   db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                   )


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
    # 外键
    author = db.relationship('User', back_populates='photos')
    comments = db.relationship('Comment', back_populates='photo', cascade='all')
    collectors = db.relationship('Collect', back_populates='collected', cascade='all')
    tags = db.relationship('Tag', secondary=tagging, back_populates='photos')


# 收藏数
class Collect(db.Model):
    # 收藏者
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    # 收藏的照片
    collected_id = db.Column(db.Integer, db.ForeignKey('photo.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    collector = db.relationship('User', back_populates='collections', lazy='joined')
    collected = db.relationship('Photo', back_populates='collectors', lazy='joined')


# 图片标签
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    # 外键
    photos = db.relationship('Photo', secondary=tagging, back_populates='tags')


# 评论
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    flag = db.Column(db.Integer, default=0)

    # 外键 评论的作者与对应照片
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'))

    photo = db.relationship('Photo', back_populates='comments')
    author = db.relationship('User', back_populates='comments')
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


# 通知
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 唯一标记
    message = db.Column(db.Text, nullable=False)  # 通知主体
    is_read = db.Column(db.Boolean, default=False)  # 是否已读
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)  # 时间戳
    # 与唯一用户建立对应关系
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 收件人id
    receiver = db.relationship('User', back_populates='notifications')





