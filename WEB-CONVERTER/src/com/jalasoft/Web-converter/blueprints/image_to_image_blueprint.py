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
from blueprints.handler import Handler1

app = Flask(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
PATH_UPLOADS = os.path.join(PATH, '../uploads')
app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'

image_blueprint = Blueprint('imagebp', __name__)


# class UploadImage(FlaskForm):  # c name and add description
#     file_image = FileField("File", validators=[InputRequired()])
#     param1_image = StringField("Param1", validators=[InputRequired()])
#     # param2_image = StringField("Param2", validators=[InputRequired()])
#     submit = SubmitField("Convert")

urls = {
    'image': 'http://127.0.0.1:5000/imagetoimage',
    'imageflip': 'http://127.0.0.1:5000/imageflip'
}


@image_blueprint.route('/image', methods=['GET', "POST"])
def image():
    form = Handler1()

    if form.validate_on_submit():

        file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                  secure_filename(file.filename))
        file.save(file_path)
        uploaded_file = open(file_path, 'rb')
        output_type = form.param1.data
        url = 'http://127.0.0.1:5000/imagetoimage'
        data = {'output_file': output_type}
        files = {'input_file': uploaded_file}
        response = requests.post(url, files=files, data=data)
        uploaded_file.close()

        if response.status_code == 200:
            download_link = response.text[:-1].strip("\"")
            return render_template('image.html', form=form, download_link=download_link)
        else:
            return "Sorry"
    return render_template('image.html', form=form)




