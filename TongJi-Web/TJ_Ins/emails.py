# -*- coding: utf-8 -*-
# @Time : 2020/11/28 14:26
# @File : emails.py
# @author : Dino
# 处理邮件发送

from threading import Thread
from flask_mail import Message
from flask import current_app, render_template
from TJ_Ins.extensions import mail


def _send_async_mail(app, message):
    with app.app_context():
        # 目前ssl版本有错误 留在之后解决
        mail.send(message)


def send_mail(to, subject, template, **kwargs):
    message = Message(current_app.config['INS_MAIL_SUBJECT_PREFIX']+subject, recipients=[to])
    message.body = render_template(template+'.txt', **kwargs)
    message.html = render_template(template+'.html', **kwargs)
    app = current_app._get_current_object()
    # 异步处理邮件发送
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


# 注册确认邮件
def send_confirm_email(user, token, to=None):
    send_mail(subject="账号注册确认邮件", to=to or user.email, template='emails/confirm', user=user, token=token)




