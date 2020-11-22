# -*- coding: utf-8 -*-
# @Time : 2020/11/21 20:05
# @File : auth.py
# @author : Dino
# 认证

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp

from TJ_Ins.models import User


# 注册表单
class RegisterForm(FlaskForm):
    # 考虑改为学号？ 算了 实名上网
    name = StringField("姓名", validators=[DataRequired(), Length(1, 30)])
    email = StringField("邮箱", validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField("用户名", validators=[DataRequired(), Length(1, 20), Regexp('^[a-zA-Z0-9\u4e00-\u9fa5]*$', message='用户名只能包含中文字符、字母大小写与数字')])
    password = PasswordField("密码", validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    passwordConfirm = PasswordField("确认密码", validators=[DataRequired()])
    submit = SubmitField()

    # 检测邮箱是否已经被使用
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("邮箱已被注册")

    # 检测用户名是否已经被使用
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("用户名已被注册")

