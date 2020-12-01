# -*- coding: utf-8 -*-
# @Time : 2020/12/1 19:51
# @File : ajax.py
# @author : Dino
# 处理网站的一些异步请求

from flask import render_template, Blueprint
from flask_login import current_user
from TJ_Ins.models import Photo, User


ajax_bp = Blueprint('ajax', __name__)


@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)
