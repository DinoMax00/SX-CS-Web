# -*- coding: utf-8 -*-
# @Time : 2020/11/21 16:25
# @File : main.py
# @author : Dino

import os
from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from flask_login import login_required, current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        # 获取浏览的页码
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['INS_PHOTO_PER_PAGE']
        pass
    else:
        pagination = None
        photos = None
    return render_template("main/index.html")
