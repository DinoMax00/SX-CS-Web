# -*- coding: utf-8 -*-
# @Time : 2020/11/21 16:25
# @File : main.py
# @author : Dino

import os
from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return 'Hello World'
