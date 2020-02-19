# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2019/12/31.
  异常：
  1.我们可以预知的异常——已知异常，抛出APIException
  2.我们没有意识到的异常——未知异常，如何统一数据的返回格式？即json格式
    解决办法：在全局的某个地方捕获到所有未知异常，统一处理未知异常——AOP
"""
from flask import request, jsonify
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we made a mistake'
    error_code = 999
    data = None

    def __init__(self, msg=None, code=None,
                 error_code=None, data=None, headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        if data:
            self.data = data
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg = self.msg,
            error_code = self.error_code,
            request = request.method + ' ' + self.get_url_no_param()
        )

        if self.data:
            body['data']= self.data

        text = str(jsonify(body).json).replace("'", '"')
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')

        return main_path[0]