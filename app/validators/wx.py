# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/2/21.
"""
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired

from app.validators.base import BaseForm as Form

class AUnlimitCodeForm(Form):
    scene = StringField(validators=[DataRequired()])
    page = StringField()
    width = IntegerField()
    auto_color = BooleanField()
    # line_color =
    is_hyaline = BooleanField()