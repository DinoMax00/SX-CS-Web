# -*- coding: utf-8 -*-
# @Time : 2020/11/21 16:25
# @File : main.py
# @author : Dino

import os
from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from flask_login import login_required, current_user
from TJ_Ins.extensions import db
from TJ_Ins.models import Photo
from TJ_Ins.utils import rename_image, resize_image

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


# 上传照片
@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':  # and 'file' in request.files:
        print("lll")
        f = request.files.get('file')  # dropzone默认上传文件属性值为file
        # 重新生成文件名
        filename = rename_image(f.filename)
        f.save(os.path.join(current_app.config['INS_UPLOAD_PATH'], filename))
        filename_s = resize_image(f, filename, current_app.config['INS_PHOTO_SIZE']['small'])
        filename_m = resize_image(f, filename, current_app.config['INS_PHOTO_SIZE']['medium'])
        photo = Photo(
            filename=filename,
            filename_s=filename_s,
            filename_m=filename_m,
            author=current_user._get_current_object()
        )
        db.session.add(photo)
        db.session.commit()
    return render_template('main/upload.html')


# 探索界面
@main_bp.route('/explore')
def explore():
    return "探索界面"
