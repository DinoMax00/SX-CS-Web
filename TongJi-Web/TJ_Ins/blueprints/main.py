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
from TJ_Ins.utils import rename_image, resize_image, flash_errors
from TJ_Ins.forms.main import CommentForm, DescriptionForm

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
    if not current_user.is_authenticated:
        return render_template('main/main_page.html')
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

    description_form.description.data = photo.description
    return render_template('main/photo.html', photo=photo, comment_form=comment_form,
                           description_form=description_form,
                           pagination=pagination, comments=comments)


# 在文件夹取出用户头像
@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename)


# 收藏照片
@main_bp.route('/collect/<int:photo_id>', methods=['POST'])
@login_required
def collect(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    # 检测是否收藏过该照片
    if current_user.is_collecting(photo):
        flash('收藏夹已有该照片', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))

    current_user.collect(photo)
    flash('收藏成功', 'success')
    return redirect(url_for('.show_photo', photo_id=photo_id))


# 取消收藏
@main_bp.route('/uncollect/<int:photo_id>', methods=['POST'])
@login_required
def uncollect(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if not current_user.is_collecting(photo):
        flash('还没有收藏', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))

    current_user.uncollect(photo)
    flash('取消成功', 'info')
    return redirect(url_for('.show_photo', photo_id=photo_id))


# 删除照片
@main_bp.route('/delete/photo/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author and current_user.username != "admin":
        abort(403)

    db.session.delete(photo)
    db.session.commit()
    flash('照片删除成功', 'info')

    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()
    if photo_n is None:
        photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()
        if photo_p is None:
            return redirect(url_for('user.index', username=photo.author.username))
        return redirect(url_for('.show_photo', photo_id=photo_p.id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))


# 发布评论
@main_bp.route('/photo/<int:photo_id>/comment/new', methods=['POST'])
@login_required
def new_comment(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    page = request.args.get('page', 1, type=int)
    form = CommentForm()
    if form.validate_on_submit():
        body = form.body.data
        author = current_user._get_current_object()
        comment = Comment(body=body, author=author, photo=photo)
        replied_id = request.args.get('reply')
        if replied_id:
            comment.replied = Comment.query.get_or_404(replied_id)

        db.session.add(comment)
        db.session.commit()
        flash('评论已发布', 'success')

    flash_errors(form)
    return redirect(url_for('.show_photo', photo_id=photo_id, page=page))


# 删除照片
@main_bp.route('/delete/comment/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if current_user != comment.author and current_user != comment.photo.author \
            and not current_user.can('MODERATE'):
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('删除成功', 'info')
    return redirect(url_for('.show_photo', photo_id=comment.photo_id))


# 对评论进行回复
@main_bp.route('/reply/comment/<int:comment_id>')
@login_required
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    return redirect(
        url_for('.show_photo', photo_id=comment.photo_id, reply=comment_id,
                author=comment.author.name) + '#comment-form')


# 用于在图片详情页面选择下一张照片与上一张照片
@main_bp.route('/photo/n/<int:photo_id>')
def photo_next(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_n = Photo.query.with_parent(photo.author).filter(Photo.id < photo_id).order_by(Photo.id.desc()).first()

    if photo_n is None:
        flash('已经是最后一张了', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_n.id))


@main_bp.route('/photo/p/<int:photo_id>')
def photo_previous(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    photo_p = Photo.query.with_parent(photo.author).filter(Photo.id > photo_id).order_by(Photo.id.asc()).first()

    if photo_p is None:
        flash('已经是第一张了', 'info')
        return redirect(url_for('.show_photo', photo_id=photo_id))
    return redirect(url_for('.show_photo', photo_id=photo_p.id))


# 编辑照片描述
@main_bp.route('/photo/<int:photo_id>/description', methods=['POST'])
@login_required
def edit_description(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if current_user != photo.author and not current_user.can('MODERATE'):
        abort(403)

    form = DescriptionForm()
    if form.validate_on_submit():
        photo.description = form.description.data
        db.session.commit()
        flash('简介已更新', 'success')

    flash_errors(form)
    return redirect(url_for('.show_photo', photo_id=photo_id))