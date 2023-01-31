#
# @handler.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms import SubmitField
from wtforms import StringField
from wtforms.validators import InputRequired


class Handler1(FlaskForm):
    """Handles the files and param received"""
    file = FileField("File", validators=[InputRequired()])
    param1 = StringField("Param1", validators=[InputRequired()])
    submit = SubmitField("Convert")


class Handler2(FlaskForm):
    """Handles the files and params received"""
    file = FileField("File", validators=[InputRequired()])
    param1 = StringField("Param1", validators=[InputRequired()])
    param2 = StringField("Param2", validators=[InputRequired()])
    submit = SubmitField("Convert")
