# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
from sqlalchemy import Column, Integer, SmallInteger, ForeignKey, orm
from app.models.base import Base
from app.models.seek_help import SeekHelp


class ErrorFeedback(Base):
    """纠错反馈"""
    id = Column(Integer, primary_key=True)
    err_type = Column(SmallInteger, nullable=False)
    msg_id = Column(Integer, ForeignKey('seek_help.id'))
    author_id = Column(Integer, ForeignKey('user.id'))


    @property
    def error_content(self):
        if self.err_type == 0:
            returned = "联系不上宠物主"
        elif self.err_type == 1:
            returned = "宠物已不需要帮助"
        elif self.err_type == 2:
            returned = "信息重复"
        else:
            returned = "其他"
        return returned