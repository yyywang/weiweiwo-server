# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
from flask import current_app, request, render_template

from app.admin import admin
from app.libs.admin_auth import admin_login_req
from app.models.seek_help import SeekHelp


@admin.route('/seek-help')
@admin_login_req
def get_seek_help():
    per_page = current_app.config['ADMIN_QUERY_NUM']
    page = request.args.get('page', 1, int)
    paginate = SeekHelp.query.filter_by().order_by(
        SeekHelp.create_time.desc()).paginate(page, per_page)
    return render_template('admin/seek_help.html',
                           active_page='seek_help', paginate=paginate)