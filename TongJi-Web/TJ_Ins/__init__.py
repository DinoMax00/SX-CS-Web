# -*- coding: utf-8 -*-
# @Time : 2020/11/21 15:39
# @File : __init__.py
# @author : Dino
# 程序运行所需的工厂函数

import os
from flask import Flask, render_template
from flask_login import current_user
from TJ_Ins.settings import config
from TJ_Ins.blueprints.main import main_bp
from TJ_Ins.blueprints.auth import auth_bp
from TJ_Ins.extensions import bootstrap, db, login_manager, dropzone, moment, csrf


# 创建实例的工厂函数 使用flask run命令时，程序就会调用该函数创建实例
def create_app(config_name=None):
    # 没有传入配置名 就从环境变量中获取，如果没有则使用默认值
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('TJ_Ins')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)

    return app


# 注册扩展
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    dropzone.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)


# 注册蓝本
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')


# 注册shell上下文处理函数
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


# 注册模板上下文处理函数

def register_template_context(app):
    pass
    """
    @app.context_processor
    def make_template_context():
        pass
    """


# 注册错误处理函数
def register_errors(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html')#, 404




