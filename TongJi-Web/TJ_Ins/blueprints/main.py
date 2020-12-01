# -*- coding: utf-8 -*-
# @Time : 2020/11/21 16:25
# @File : main.py
# @author : Dino

import os
from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from TJ_Ins.extensions import db
from TJ_Ins.models import Photo, User, Collect, Comment, Tag, Follow
from TJ_Ins.utils import rename_image, resize_image
from TJ_Ins.forms.main import CommentForm, TagForm, DescriptionForm

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        # 获取浏览的页码
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['INS_PHOTO_PER_PAGE']
        # 使用paginate函数进行分页
        pagination = Photo.query.order_by(Photo.timestamp.desc()).paginate(page, per_page)
        photos = pagination.items
    else:
        pagination = None
        photos = None
    tags = Tag.query.join(Tag.photos).group_by(Tag.id).order_by(func.count(Photo.id).desc()).limit(10)
    return render_template('main/index.html', pagination=pagination, photos=photos, tags=tags, Collect=Collect)


# 上传照片
@main_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':  # and 'file' in request.files:
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
    # 四行三列 随机取12张图
    # html中有一个change按钮，实质上是重新进入explore页面 再随机生成几张（因此可能会重复之前展示过的图片）
    photos = Photo.query.order_by(func.random()).limit(12)
    return render_template('main/explore.html', photos=photos)


# 生成图片下载链接
@main_bp.route('/uploads/<path:filename>')
def get_image(filename):
    # flask中的send_from_directory函数可以从文件夹上传图片
    return send_from_directory(current_app.config['INS_UPLOAD_PATH'], filename)


# 图片点击后的详情界面
@main_bp.route('/photo/<int:photo_id>')
def show_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['INS_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(photo).order_by(Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items

    comment_form = CommentForm()
    description_form = DescriptionForm()
    tag_form = TagForm()

    description_form.description.data = photo.description
    return render_template('main/photo.html', photo=photo, comment_form=comment_form,
                           description_form=description_form, tag_form=tag_form,
                           pagination=pagination, comments=comments)


# 在文件夹取出用户头像
@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)







