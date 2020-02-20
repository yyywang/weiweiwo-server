# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
import click
from werkzeug.exceptions import HTTPException
from app import create_app
from app.libs.error import APIException
from app.libs.error_code import ServerError
from app.models.admin import Admin
from app.models.base import db

__author__ = "怀月"

app = create_app()

@app.errorhandler(Exception)
def framework_error(e):
    # 处理APIException
    if isinstance(e, APIException):
        return e
    # 处理HTTPException
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    # 处理Exception
    else:
        if not app.config['DEBUG']:
            return ServerError()
        else:
            raise e

if __name__ == '__main__':
    # app.run(host='127.0.0.1',port=5009,debug=True)
    app.run(host='0.0.0.0', port=5009, debug=True)


@app.cli.command('create_admin')
@click.option("--account", prompt='请输入账号')
@click.option("--pwd", prompt='请输入密码', hide_input=True)
@click.option("--repwd", prompt='请再次输入密码', hide_input=True)
def create_admin(account, pwd, repwd):
    """
    创建初始 admin
    :return:
    """
    if pwd == repwd:
        with db.auto_commit():
            admin = Admin()
            admin.account = account
            admin.password = pwd
            db.session.add(admin)
            click.echo(account + ' 已成功创建')
    else:
        click.echo('两次密码不同，请重新输入')
        return


@app.cli.command('forbid_admin')
@click.option('--account', prompt='请输入账号')
def forbid_admin(account):
    """
    禁用amdin
    :param account: 
    :return: 
    """
    admin = Admin.query.filter_by(account=account).first()
    with db.auto_commit():
        admin.status = False
        db.session.add(admin)
        click.echo(account + ' 已禁用')
    return