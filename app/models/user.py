# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/31.
"""
from sqlalchemy import Column, Integer, String, SmallInteger
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.error_code import AuthFailed, Success, Forbidden
from app.models.base import Base, db, MixinJSONSerializer
from app.libs.wx import wx_get_user_by_code
from app.models.boost_seek_help import BoostSeekHelp


class User(Base, MixinJSONSerializer):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True)
    nickname = Column(String(24), unique=True) # 邮箱注册的昵称
    auth = Column(SmallInteger, default=1)  # 权限类型，1 代表普通用户
    _password = Column('password', String(1000))
    seek_helps = relationship('SeekHelp', backref='author')
    seek_help_update_logs = relationship('SeekHelpUpdateLog', backref='operator')
    error_feedbacks = relationship('ErrorFeedback', backref='author')
    boosts = relationship('BoostSeekHelp', backref='helper')
    rescues = relationship('Rescue', backref='author') # 我能帮
    wx_open_id = Column(String(255), unique=True)
    wx_name = Column(String(255))
    wx_avatar = Column(String(255))
    gender = Column(SmallInteger) # 性别：0-未知；1-男性；2-女性

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    # 因为此方法在类User中创建了User实例
    # 所以将此方法定义为静态方法，即：staticmethod
    @staticmethod
    def register_by_email(nickname, account, password):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = password
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email) \
            .first_or_404(description="user not found")
        if not user.check_password(password):
            raise AuthFailed()
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self.password:
            return False
        return check_password_hash(self.password, raw)

    @staticmethod
    def verify_mina(account, secret):
        """
        校验小程序是否已注册
        :param account: 小程序 code
        :param secret: None
        :return: 
        """
        openid = wx_get_user_by_code(account)['openid']
        user = User.query.filter_by(wx_open_id=openid) \
            .first_or_404(description="user not found")
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    @staticmethod
    def register_by_mina(wx_open_id):
        user = User.query.filter_by(wx_open_id=wx_open_id).first()
        if user:
            raise Forbidden(msg='openid has been registered')
        else:
            with db.auto_commit():
                user = User()
                user.wx_open_id = wx_open_id
                db.session.add(user)
            return Success()

    def _set_fields(self):
        self._fields = ['id', 'wx_name', 'wx_avatar']

    def verify_boost(self, seek_help):
        """1. 校验用户是否已助力某 seek_help
            2. 校验用户是否是发求助信息者"""
        if BoostSeekHelp.query.filter_by(helper_id=self.id, seek_help_id=seek_help.id).first():
            raise Forbidden(msg='already boost')
        if seek_help.author_id == self.id:
            raise Forbidden(msg="can't help yourself")
