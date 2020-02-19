# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/10.
"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

from app.admin import auth
from app.admin import feedback
from app.admin import main
from app.admin import seek_help