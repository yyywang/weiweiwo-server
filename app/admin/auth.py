# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
from flask import request, session, url_for, redirect, flash, render_template
from app.admin import admin
from app.libs.admin_auth import admin_login_req
from app.models.admin import Admin
from app.validators.auth import AdminLoginForm


@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm(request.form)
    if request.method == 'POST' and form.validate():
        obj_admin = Admin.query.filter_by(account=form.account.data).first()
        if obj_admin and obj_admin.check_password(form.password.data):
            # login_user 为 flask-login 插件的组件
            # 将用户信息写入 cookie 中，即：登录
            # admin_log()
            if form.remember.data:
                session['admin'] = obj_admin.account
                session['admin_id'] = obj_admin.id
                session.permanent = True
            else:
                session['admin'] = obj_admin.account
                session['admin_id'] = obj_admin.id
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                # 登录后跳转上个需登录才能访问的页面，若无则跳转至首页
                # not next_page.startswith('/') 防止重定向攻击
                next_page = url_for('admin.index')
            return redirect(next_page)
        else:
            flash('用户不存在或密码错误', 'danger')
    return render_template('admin/login.html', form=form)


@admin.route("/logout")
@admin_login_req
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))