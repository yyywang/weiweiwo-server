# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
from datetime import date
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder
from app.libs.error_code import ServerError


class JSONEncoder(_JSONEncoder):
    def default(self, o):
        """
        如果遇到不能序列化的数据，在下面添加if语句进行序列化
        :param o: 序列化的源数据
        :return: 
        """
        if hasattr(o, 'keys') and hasattr(o, '__getitem__'):
            return dict(o)
        if isinstance(o, date):
            return o.strftime('%Y-%m-%d')
        raise ServerError()


class Flask(_Flask):
    json_encoder = JSONEncoder