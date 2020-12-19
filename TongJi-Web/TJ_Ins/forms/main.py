# -*- coding: utf-8 -*-
# @Time : 2020/11/28 9:42
# @File : main.py
# @author : Dino
# 主页表单

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


# 评论表单
class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired(message='回复不能为空')])
    submit = SubmitField('发布')


# 图片介绍
class DescriptionForm(FlaskForm):
    description = TextAreaField('简介', validators=[Optional(), Length(0, 500)])
    submit = SubmitField('发布')