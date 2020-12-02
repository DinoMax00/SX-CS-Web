# -*- coding: utf-8 -*-
# @Time : 2020/11/21 15:39
# @File : __init__.py
# @author : Dino
# 程序运行所需的工厂函数

import os
import click
from flask import Flask, render_template
from flask_login import current_user
from TJ_Ins.settings import config
from TJ_Ins.blueprints.main import main_bp
from TJ_Ins.blueprints.auth import auth_bp
from TJ_Ins.blueprints.user import user_bp
from TJ_Ins.extensions import bootstrap, db, login_manager, dropzone, moment, csrf, avatars


# 创建实例的工厂函数 使用flask run命令时，程序就会调用该函数创建实例
def create_app(config_name=None):
    # 没有传入配置名 就从环境变量中获取，如果没有则使用默认值
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask('TJ_Ins')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errorhandles(app)
    register_shell_context(app)
    register_template_context(app)
    register_commands(app)

    return app


# 注册扩展
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    dropzone.init_app(app)
    moment.init_app(app)
    csrf.init_app(app)
    avatars.init_app(app)


# 注册蓝本
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')


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
def register_errorhandles(app):
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html'), 404


# 注册命令行窗口的命令
def register_commands(app):
    # 数据库初始化
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='初始化前删除旧库')  # 增加一个输入参数，通过is_flag设为bool类型
    def initdb(drop):
        if drop:
            click.confirm("这个操作将删除之前的数据库，确认继续吗？", abort=True)
            db.drop_all()
            click.echo("删除成功")
        db.create_all()
        click.echo("初始化数据库成功")

    # 玩一下
    @app.cli.command()
    @click.option('--喵喵', is_flag=True, help='miao~')  # 增加一个输入参数，通过is_flag设为bool类型
    def 喵(喵喵):
        if 喵喵:
            click.confirm("喵喵", abort=True)
            db.drop_all()
            click.echo("喵喵喵")
        db.create_all()
        click.echo("喵喵喵喵")
