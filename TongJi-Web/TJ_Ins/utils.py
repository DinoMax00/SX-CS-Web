# -*- coding: utf-8 -*-
# @Time : 2020/11/22 22:52
# @File : utils.py
# @author : Dino
# 一些组件函数

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin
from flask import current_app, request, url_for, redirect, flash


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
