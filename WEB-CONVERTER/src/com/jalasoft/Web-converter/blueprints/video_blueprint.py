from flask import Blueprint
import os
import requests
from flask import Flask
from flask import render_template
from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
from wtforms import FileField
from wtforms import SubmitField
from wtforms import StringField
from wtforms.validators import InputRequired
from blueprints.handler import Handler2

video_blueprint = Blueprint('video', __name__)
app = Flask(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
PATH_UPLOADS = os.path.join(PATH, '../uploads')
app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'


# class UploadVideo(FlaskForm):  # c name and add description
#     file_video = FileField("File", validators=[InputRequired()])
#     param1_video = StringField("Param1", validators=[InputRequired()])
#     param2_video = StringField("Param2", validators=[InputRequired()])
#     submit = SubmitField("Convert")


@video_blueprint.route('/video', methods=['GET', "POST"])
def video():
    form = Handler2()

    if form.validate_on_submit():

        file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                 secure_filename(file.filename))
        file.save(file_path)
        uploaded_file = open(file_path, 'rb')
        output_type = form.param1.data
        fps = form.param2.data
        url = 'http://127.0.0.1:5000/videotoimage/zip'
        data = {'output_file': output_type, 'fps': fps}
        files = {'input_file': uploaded_file}
        response = requests.post(url, files=files, data=data)
        uploaded_file.close()
        print(response)
        if response.status_code == 200:
            download_link = response.text[:-1].strip("\"")
            return render_template('video.html', form=form, download_link=download_link, output_file = output_type)
        else:
            return "Sorry video"
    return render_template('video.html', form=form)


