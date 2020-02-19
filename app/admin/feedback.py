# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
from flask import current_app, request, render_template
from sqlalchemy import and_

from app.admin import admin
from app.libs.admin_auth import admin_login_req
from app.models.error_feedback import ErrorFeedback
from app.models.seek_help import SeekHelp


@admin.route('/feedback')
@admin_login_req
def get_feedback():
    per_page = current_app.config['ADMIN_QUERY_NUM']
    page = request.args.get('page', 1, int)
    # paginate = ErrorFeedback.query.filter_by().order_by(
    #     ErrorFeedback.create_time.desc()).paginate(page, per_page)
    paginate = ErrorFeedback.query.join(SeekHelp).filter(
        and_(SeekHelp.status == 1, ErrorFeedback.status == 1)).order_by(
        ErrorFeedback.create_time.desc()).paginate(page, per_page)
    return render_template('admin/feedback.html',
                           active_page='feedback', paginate=paginate)