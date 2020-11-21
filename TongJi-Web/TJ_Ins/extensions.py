# -*- coding: utf-8 -*-
# @Time : 2020/11/21 16:01
# @File : extensions.py
# @author : Dino
# 进行扩展实例化

from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, AnonymousUserMixin
from flask_dropzone import Dropzone
from flask_wtf import CSRFProtect


bootstrap = Bootstrap()
# 数据库
ab = SQLAlchemy()
# 登录
login_manager = LoginManager()
# 图片上传
dropzone = Dropzone()
moment = Moment()
csrf = CSRFProtect()
