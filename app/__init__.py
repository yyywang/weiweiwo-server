# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/7.
"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask import request
from app.app import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')
    register_blueprints(app)
    register_plugin(app)
    register_logging(app)

    return app


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    from app.admin import admin
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
    app.register_blueprint(admin, url_prefix='/admin')


def register_plugin(app):
    from app.models.base import db
    from flask_migrate import Migrate
    # from flask_debugtoolbar import DebugToolbarExtension
    from flask_apscheduler import APScheduler

    db.init_app(app)
    migrate = Migrate()
    migrate.init_app(app=app, db=db)
    # toolbar = DebugToolbarExtension()
    # toolbar.init_app(app)
    # scheduler = APScheduler()
    # scheduler.init_app(app)
    # scheduler_add_job(scheduler) # 添加定时任务
    # scheduler.start()
    with app.app_context():
        db.create_all()


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)


    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    file_handler = RotatingFileHandler(os.path.join(basedir, 'app/logs/wuhan.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    default_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)
        app.logger.addHandler(default_handler)


def scheduler_add_job(scheduler):
    """添加定时任务"""
    pass