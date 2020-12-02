# -*- coding: utf-8 -*-
# @Time : 2020/11/22 22:52
# @File : utils.py
# @author : Dino
# 一些组件函数

# 根据拥有的模块，导入函数
try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
import PIL
import os
import uuid
from PIL import Image
from flask import current_app, request, url_for, redirect, flash
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from TJ_Ins.models import User
from TJ_Ins.extensions import db
from TJ_Ins.settings import Operations


# 是否是安全链接
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# 登录后的页面跳转
def redirect_back(default='main.index', **kwargs):
    # request中的next参数保存了 跳转前想访问的地址
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    # 没有next参数就跳回主页
    return redirect(url_for(default, **kwargs))


# 将图片名改为随机数表示
def rename_image(old_filename):
    ext = os.path.splitext(old_filename)[1]
    new_filename = uuid.uuid4().hex + ext
    return new_filename


# 设置图片大小
def resize_image(image, filename, base_width):
    # 分离文件名与扩展名
    filename, ext = os.path.splitext(filename)
    img = Image.open(image)
    if img.size[0] <= base_width:
        return filename + ext
    # 以宽度为基准，按比例缩放
    w_percent = (base_width / float(img.size[0]))
    h_size = int((float(img.size[1]) * float(w_percent)))
    img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)

    filename += current_app.config['INS_PHOTO_SUFFIX'][base_width] + ext
    img.save(os.path.join(current_app.config['INS_UPLOAD_PATH'], filename), optimize=True, quality=85)
    return filename


# 表单连续报错(闪现)
def flash_errors(form):
    # 循环表单中的所有错误
    for field, errors in form.errors.items():
        # 循环所有错误
        for error in errors:
            flash(u"Error in the %s field - %s" % (getattr(form, field).label.text,error))

