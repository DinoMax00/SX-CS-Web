# -*- coding: utf-8 -*-
# @Time : 2020/11/23 9:07
# @File : app.py
# @author : Dino
from flask import Flask, app, render_template

app = Flask(__name__)


@app.route('/1')
def test():
    return "nnn"
