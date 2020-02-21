# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/21.
"""
from app.models.base import db
from app.models.staging import Staging


def get_value_by_key(key):
    """通过 key 在暂存数据表获取值"""
    returned = None
    obj_staging = Staging.query.filter_by(key=key).first()
    if obj_staging and not obj_staging.is_expire():
        returned = obj_staging.value
    return returned


def set_value_by_key(key, value, expires_at, des):
    """通过 key 设置暂存数据表中的值"""
    obj_staging = Staging.query.filter_by(key=key).first()
    # 若暂存区已存在此参数则进行更新
    if obj_staging:
        with db.auto_commit():
            obj_staging.value = value
            if expires_at:
                obj_staging.expires_at = expires_at
    # 若暂存区不存在此参数则新建
    else:
        with db.auto_commit():
            obj_staging = Staging()
            obj_staging.key = key
            obj_staging.value = value
            obj_staging.expires_at = expires_at
            obj_staging.des = des
            db.session.add(obj_staging)