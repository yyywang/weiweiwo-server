# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
from flask import current_app
from itsdangerous import Serializer
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.base import Base, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


class Admin(Base):
    id = Column(Integer, primary_key=True)
    account = Column(String(24), nullable=False, unique=True)
    _password = Column('password', String(128), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        """
        加密明文密码
        :param raw: 原始密码
        :return: 
        """
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    def generate_token(self, expiration=600):
        """
        生成token
        :param expiration: 默认过期时间为600秒
        :return: 
        """
        # 序列化器
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(new_password):
        with db.auto_commit():
            obj_admin = Admin.query.first()
            if not obj_admin:
                return False
            obj_admin.password = new_password
        return True