# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/20.
"""
from app.models.rescue import Rescue
from app.models.seek_help import SeekHelp

def supplicant_num():
    """平台总寻求救助人"""
    return SeekHelp.query.group_by(SeekHelp.author_id).count()

def rescuer_num():
    """平台总营救人"""
    return Rescue.query.group_by(Rescue.author_id).count()

def get_boost_data():
    return dict(
        supplicant_num=supplicant_num(),
        rescuer_num=rescuer_num()
    )