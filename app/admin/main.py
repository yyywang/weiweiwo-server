# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
from app.admin import admin
from app.libs.admin_auth import admin_login_req
from flask import redirect, url_for


@admin.route('/')
@admin_login_req
def index():
    return redirect(url_for('admin.get_feedback'))