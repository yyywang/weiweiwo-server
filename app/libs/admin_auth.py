# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
# 登录装饰器
from functools import wraps
from flask import session, redirect, url_for, request, flash


def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            flash('请先登录', 'danger')
            return redirect(url_for("admin.login", next=request.url), )
        return f(*args, **kwargs)

    return decorated_function