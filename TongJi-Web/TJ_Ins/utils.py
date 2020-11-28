# -*- coding: utf-8 -*-
# @Time : 2020/11/22 22:52
# @File : utils.py
# @author : Dino
# 一些组件函数

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


# 生成token
def generate_token(user, operation, expire_in=None, **kwargs):
    s = Serializer(current_app.config['SECRET_KEY'], expire_in)

    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return s.dumps(data)


# 验证token
def validate_token(user, token, operation, new_password=None):
    s = Serializer(current_app.config['SECRET_KEY'])

    try:
        data = s.loads(token)
    except (SignatureExpired, BadSignature):
        return False

    if operation != data.get('operation') or user.id != data.get('id'):
        return False

    if operation == Operations.CONFIRM:
        user.confirmed = True
    elif operation == Operations.RESET_PASSWORD:
        user.set_password(new_password)
    elif operation == Operations.CHANGE_EMAIL:
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        user.email = new_email
    else:
        return False

    db.session.commit()
    return True


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
