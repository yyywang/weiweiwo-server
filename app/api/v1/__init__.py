# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/30.
"""
from flask import Blueprint
from app.api.v1 import user, client, token, seek_help, rescue, common


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    # 将 Redprint 注册到蓝图 v1
    user.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    seek_help.api.register(bp_v1)
    rescue.api.register(bp_v1)
    common.api.register(bp_v1)

    return bp_v1