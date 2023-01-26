from flask_wtf import FlaskForm
from wtforms import FileField
from wtforms import SubmitField
from wtforms import StringField
from wtforms.validators import InputRequired


class Handler1(FlaskForm):  # c name and add description
    file = FileField("File", validators=[InputRequired()])
    param1 = StringField("Param1", validators=[InputRequired()])
    submit = SubmitField("Convert")


class Handler2(FlaskForm):  # c name and add description
    file = FileField("File", validators=[InputRequired()])
    param1 = StringField("Param1", validators=[InputRequired()])
    param2 = StringField("Param2", validators=[InputRequired()])
    submit = SubmitField("Convert")



