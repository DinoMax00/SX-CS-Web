# -*- coding: utf-8 -*-
# @Time : 2020/12/1 19:51
# @File : ajax.py
# @author : Dino
# 处理网站的一些异步请求

from flask import render_template, Blueprint, jsonify
from flask_login import current_user
from TJ_Ins.models import Photo, User


ajax_bp = Blueprint('ajax', __name__)


# 实现鼠标移动到头像时，显示个人信息的效果
@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)


# 异步发送收藏图片的请求
@ajax_bp.route('/collect/<int:photo_id>', methods=['POST'])
def collect(photo_id):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录'), 403

    photo = Photo.query.get_or_404(photo_id)
    if current_user.is_collecting(photo):
        return jsonify(message='图片已在收藏夹中'), 400

    current_user.collect(photo)
    return jsonify(message='收藏成功')


@ajax_bp.route('/uncollect/<int:photo_id>', methods=['POST'])
def uncollect(photo_id):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录'), 403

    photo = Photo.query.get_or_404(photo_id)
    if not current_user.is_collecting(photo):
        return jsonify(message='图片不在收藏夹中'), 400

    current_user.uncollect(photo)
    return jsonify(message='取消成功')


# 异步返回
@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    user = User.query.get_or_404(user_id)
    count = user.followers.count() - 1
    return jsonify(count=count)


@ajax_bp.route('/<int:photo_id>/followers-count')
def collectors_count(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    count = len(photo.collectors)
    return jsonify(count=count)


@ajax_bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    if not current_user.is_authenticated:
        return jsonify(message='请先登录'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        return jsonify(message='还没有关注'), 400

    current_user.unfollow(user)
    return jsonify(message='取消成功')
