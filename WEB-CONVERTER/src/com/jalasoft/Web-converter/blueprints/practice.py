# main.py:
import os
import requests
from flask import Flask, Blueprint
from flask import render_template
# from flask_wtf import FlaskForm
from werkzeug.utils import secure_filename
# from wtforms import FileField
# from wtforms import SubmitField
# from wtforms import StringField
# from wtforms.validators import InputRequired
from handle_inputs import Handler2, Handler1


video_to_images_blueprint = Blueprint('video_to_images', __name__)
video_to_video_blueprint = Blueprint('video_to_video', __name__)

app = Flask(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
PATH_UPLOADS = os.path.join(PATH, '../uploads')
app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'


@video_to_images_blueprint.route('/video_to_images', methods = ['GET', "POST"])
def video_to_images():
    """Manages endpoint for video to images converter"""
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
        response = requests.post(url, files = files, data = data)
        uploaded_file.close()
        if response.status_code == 200:
            download_link = response.text[:-1].strip("\"")
            return render_template('video_to_images.html', form = form, download_link = download_link, output_file = output_type)
    return render_template('video_to_images.html', form = form)


@video_to_video_blueprint.route('/video_to_video', methods = ['GET', "POST"])
def video_to_video():
    """Manages endpoint for video to video converter"""
    form = Handler1()
    if form.validate_on_submit():
        file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                 secure_filename(file.filename))
        file.save(file_path)
        uploaded_file = open(file_path, 'rb')
        output_type = form.param1.data
        url = 'http://127.0.0.1:5000/videotovideo'
        data = {'output_file': output_type}
        files = {'input_file': uploaded_file}
        response = requests.post(url, files = files, data = data)
        uploaded_file.close()
        if response.status_code == 200:
            download_link = response.text[:-1].strip("\"")
            return render_template('video_to_video.html', form = form, download_link = download_link, output_file = output_type)
    return render_template('video_to_video.html', form = form)


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    """Manages home's page"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True, port = 5017)

app.register_blueprint(video_to_images_blueprint)
app.register_blueprint(video_to_video_blueprint)
