# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/20.
"""
from app.models.rescue import Rescue
from app.models.seek_help import SeekHelp
from app.models.seek_help_update_log import SeekHelpUpdateLog


def supplicant_num():
    """平台总寻求救助人数"""
    return SeekHelp.query.group_by(SeekHelp.author_id).count()

def rescuer_num():
    """平台总愿意帮助人数"""
    return Rescue.query.group_by(Rescue.author_id).count()

def life_num():
    """平台总被营救过的宠物数"""
    return SeekHelpUpdateLog.query.group_by(SeekHelpUpdateLog.seek_help_id).count()


def get_boost_data():
    return dict(
        supplicant_num=supplicant_num(),
        rescuer_num=rescuer_num(),
        life_num=life_num()
    )