# -*- coding: utf-8 -*-
# @Time : 2020/11/21 14:45
# @File : settings.py
# @author : Dino
# 使用类组织配置

import os
import sys

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# win与linux数据库URI有所不同
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


# 邮箱验证的三种操作
class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'


# 基本配置
class BaseConfig:
    # 基本参数
    INS_PHOTO_PER_PAGE = 12
    INS_MAIL_SUBJECT_PREFIX = '[TJ-Ins]'
    INS_UPLOAD_PATH = os.path.join(basedir, 'uploads')  # 图片存放路径
    INS_PHOTO_SIZE = {'small': 400, 'medium': 800}  # 两类图片大小 分别用于explore与主页
    INS_COMMENT_PER_PAGE = 15  # 图片详情页的最大评论数
    INS_PHOTO_SUFFIX = {INS_PHOTO_SIZE['small']: '_s',
                        INS_PHOTO_SIZE['medium']: '_m'}
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')

    # dropzone相关
    DROPZONE_INPUT_NAME = "file"
    DROPZONE_ALLOWED_FILE_TYPE = 'image'
    DROPZONE_MAX_FILE_SIZE = 3  # 3MB
    DROPZONE_MAX_FILES = 30
    DROPZONE_ENABLE_CSRF = True

    # avatar相关
    AVATARS_SAVE_PATH = os.path.join(INS_UPLOAD_PATH, 'avatars')  # 头像存放链接
    AVATAR_SIZE = (30, 100, 200)  # 三个尺寸的头像

    # 关闭数据库警告信息
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BOOTSTRAP_SERVE_LOCAL = True


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = \
        prefix + os.path.join(basedir, 'data-dev.db')
    REDIS_URL = "redis://localhost"


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
