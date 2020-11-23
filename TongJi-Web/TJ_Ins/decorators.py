# -*- coding: utf-8 -*-
# @Time : 2020/11/22 22:01
# @File : decorators.py
# @author : Dino
# 一些装饰器

from functools import wraps

from flask import Markup, flash, url_for, redirect, abort
from flask_login import current_user


