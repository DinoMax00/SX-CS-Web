# -*- coding: utf-8 -*-
# @Time : 2020/11/30
# @File : user.py
# @author : Ray

# 导入公共库
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, HiddenField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional, Regexp
# 导入自定义库
from TJ_Ins.models import User


# 编辑用户资料的表单
class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 30)])
    username = StringField('用户名', validators=[DataRequired(),
                                              Length(1, 20),
                                              Regexp('^[a-zA-Z0-9\u4e00-\u9fa5]*$', message='用户名只能包含中文字符、字母大小写与数字')])

    website = StringField('个人主页', validators=[Optional(), Length(0, 255),
                                              Regexp('(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,'
                                                     '@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',
                                                     message='请输入您的主页链接(http或https开头)')])
    location = StringField('城市', validators=[Optional(), Length(0, 50)])
    bio = TextAreaField('个人简介', validators=[Optional(), Length(0, 120)])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已注册')


# 上传图片的表单
class UploadAvatarForm(FlaskForm):
    image = FileField('上传', validators=[FileRequired(), FileAllowed(['jpg', 'png'], '文件格式必须是\'.jpg\'或\'.png\'')])
    submit = SubmitField('提交')


# 更改邮箱地址的表单
class ChangeEmailForm(FlaskForm):
    email = StringField('新的邮箱地址', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField('提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('该邮箱已被注册')


# 更改密码的表单
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('再次输入新密码', validators=[DataRequired()])
    submit = SubmitField('提交')

# 删除账户的表单
class DeleteAccountForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField('提交')

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('用户名输入错误')


# 修改头像
class CropAvatarForm(FlaskForm):
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('裁剪并上传')
