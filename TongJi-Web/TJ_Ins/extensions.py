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
from flask_avatars import Avatars

bootstrap = Bootstrap()
db = SQLAlchemy()  # 数据库
login_manager = LoginManager()  # 登录
dropzone = Dropzone()  # 图片上传
moment = Moment()
csrf = CSRFProtect()  # csrf验证
avatars = Avatars()  # 虚拟头像


# 用户加载函数 返回当前登录用户
@login_manager.user_loader
def load_user(user_id):
    from TJ_Ins.models import User
    user = User.query.get(int(user_id))
    return user
