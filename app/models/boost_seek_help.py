# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/18.
"""
from sqlalchemy import Column, Integer, ForeignKey
from app.models.base import MixinJSONSerializer, Base


class BoostSeekHelp(Base, MixinJSONSerializer):
    id = Column(Integer, primary_key=True)
    helper_id = Column(Integer, ForeignKey('user.id'))
    seek_help_id = Column(Integer, ForeignKey('seek_help.id'))
