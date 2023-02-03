from flask import Blueprint
import os
import requests
from flask import Flask
from flask import render_template
from werkzeug.utils import secure_filename
from blueprints.handler import Handler2

handler = Handler2
app = Flask(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
PATH_UPLOADS = os.path.join(PATH, '../uploads')
app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'


class ConverterBase:
    def __init__(self, url, form):
        self.url = url
        self.form = form
        self.file = form.file.data
        self.file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], secure_filename(self.file.filename))
        self.output_type = form.param1.data
        self.app = Flask(__name__)
        PATH = os.path.realpath(os.path.dirname(__file__))
        PATH_UPLOADS = os.path.join(PATH, '../uploads')
        self.app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
        self.app.config['SECRET_KEY'] = 'supersecretkey'

    def upload_file(self):
        self.file.save(self.file_path)
        uploaded_file = open(self.file_path, 'rb')
        files = {'input_file': uploaded_file}
        response = requests.post(self.url, files = files, data = self.data)
        uploaded_file.close()
        return response


video_to_images_blueprint = Blueprint('video_to_images', __name__)


class VideoToImagesConverter(ConverterBase):
    def __init__(self, form):
        super().__init__(url='http://127.0.0.1:5000/videotoimage/zip', form=form)
        self.fps = form.param2.data
        self.data = {'output_file': self.output_type, 'fps': self.fps}

    @video_to_images_blueprint.route('/video_to_images', methods = ['GET', "POST"])
    def handle_request(self):
        """Manages endpoint for video to images converter"""
        if self.form.validate_on_submit():
            response = self.upload_file()
            if response.status_code == 200:
                download_link = response.text[:-1].strip("\"")
                return render_template('video_to_images.html', form = self.form, download_link = download_link, output_file = self.output_type)
        return render_template('video_to_images.html', form = self.form)

