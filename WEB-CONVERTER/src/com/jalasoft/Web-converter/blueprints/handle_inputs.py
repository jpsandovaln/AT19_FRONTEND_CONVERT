#
# @handle_inputs.py Copyright (c) 2023 Jalasoft.
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
from wtforms.validators import InputRequired, Optional


class HandleInputs(FlaskForm):
    """Handles the files and parameters received for conversion"""
    file = FileField("File", validators=[InputRequired()])
    param1 = StringField("Param1", validators=[InputRequired()])
    param2 = StringField("Param2", validators=[Optional()])
    submit = SubmitField("Convert")

