#
# @video_to_images_bp.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask import Blueprint
import os
import requests
from flask import Flask
from flask import render_template
from werkzeug.utils import secure_filename
from blueprints.handler import Handler2

video_to_images_blueprint = Blueprint('video_to_images', __name__)

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
        else:
            return "Sorry"  #
    return render_template('video_to_images.html', form = form)


