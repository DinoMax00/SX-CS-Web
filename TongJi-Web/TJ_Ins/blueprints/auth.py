# -*- coding: utf-8 -*-
# @Time : 2020/11/22 22:10
# @File : auth.py
# @author : Dino
# 处理认证视图

from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user, login_fresh, confirm_login

from TJ_Ins.forms.auth import LoginForm, RegisterForm
from TJ_Ins.models import User
from TJ_Ins.utils import redirect_back
from TJ_Ins.extensions import db
auth_bp = Blueprint('auth', __name__)


# 登录
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        # 数据库查询邮箱信息
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.validate_password(form.password.data):
            if login_user(user, form.remember_me.data):
                flash('登陆成功', 'info')
                return redirect_back()
            else:
                flash('您的账户已被冻结', 'warning')
                return redirect(url_for('main.index'))
        flash('邮箱或密码错误', 'warning')
    return render_template('auth/login.html', form=form)


# 登出
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出登录成功', 'info')
    return redirect(url_for('main.index'))


# 注册
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        # 生成数据库类型
        user = User(name=name, email=email, username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)
