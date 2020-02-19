# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/30.
"""


class Redprint:
    def __init__(self, name):
        self.name = name
        # 由于 Redprint 无法直接 add_url_rule
        # 所以先将参数保存下来，后面再添加
        # 使用数组：mound 保存
        self.mound = []

    def route(self, rule, **options):
        def decorator(f):
            self.mound.append((f, rule, options))
            return f

        return decorator

    def register(self, bp, url_prefix=None):
        # 优化：不传 prefix 自动使用 Redprint 名作为 prefix
        if url_prefix is None:
            url_prefix = '/' + self.name
        for f, rule, options in self.mound:
            # 如果 options 字典中没有 endpoint 元素，那么取 f.__name__ 的值
            # 想当于为 endpoint 添加了默认值
            endpoint = self.name + '+' + \
                       options.pop("endpoint", f.__name__)
            bp.add_url_rule(url_prefix + rule, endpoint, f, **options)
