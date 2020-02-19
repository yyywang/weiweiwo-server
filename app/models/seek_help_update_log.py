# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/18.
"""
from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import Base, MixinJSONSerializer


class SeekHelpUpdateLog(Base, MixinJSONSerializer):
    id = Column(Integer, primary_key=True)
    operator_id = Column(Integer, ForeignKey('user.id'))
    seek_help_id = Column(Integer, ForeignKey('seek_help.id'))
    old_help_date = Column(Integer) # 更新之前的 需要帮助日期
    new_help_date = Column(Integer) # 更新之后的 需要帮助日期
    old_last_date = Column(Integer) # 更新之前的 最后帮助日期
    new_last_date = Column(Integer) # 更新之后的 最后帮助日期
