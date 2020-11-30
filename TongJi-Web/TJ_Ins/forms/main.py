# -*- coding: utf-8 -*-
# @Time : 2020/11/28 9:42
# @File : main.py
# @author : Dino
# 主页表单

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length


# 评论表单
class CommentForm(FlaskForm):
    body = TextAreaField('', validators=[DataRequired()])
    submit = SubmitField()


# 图片介绍
class DescriptionForm(FlaskForm):
    description = TextAreaField('Description', validators=[Optional(), Length(0, 500)])
    submit = SubmitField()


# 图片标签
class TagForm(FlaskForm):
    tag = StringField('Add Tag (use space to separate)', validators=[Optional(), Length(0, 64)])
    submit = SubmitField()
