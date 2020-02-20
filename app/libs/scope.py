# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/1/4.
  对接口的访问权限控制
"""
class Scope:
    allow_api = [] # 允许访问的视图函数
    allow_module = [] # 允许访问该模块下的所有视图函数
    forbidden_api = [] # 禁止访问此视图函数

    def __add__(self, other):
        """重载 + 运算符"""
        self.allow_api = self.allow_api + other.allow_api
        self.allow_api = list(set(self.allow_api)) # 利用set去重

        self.allow_module = self.allow_module + other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden_api = self.forbidden_api + other.forbidden_api
        self.forbidden_api = list(set(self.forbidden_api))
        return self # 返回对象自身，以支持链式调用


class AdminScope(Scope):
    # allow_api = ['v1.super_get_user']
    allow_module = ['v1.user']
    def __init__(self):
        self + UserScope()


class UserScope(Scope):
    allow_api = ['v1.user+get_user', 'v1.user+delete_user', 'v1.user+update_user',
                 'v1.user+get_seek_help_list', 'v1.user+get_seek_help', 'v1.user+get_rescue_list',
                 'v1.user+cancel_or_not_seek_help', 'v1.user+get_rescue', 'v1.user+cancel_or_not_rescue']

    allow_module = ['v1.seek-help', 'v1.rescue', 'v1.common']



def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden_api:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False