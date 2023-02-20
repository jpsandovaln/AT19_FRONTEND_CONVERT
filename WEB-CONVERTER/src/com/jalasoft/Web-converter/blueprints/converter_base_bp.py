#
# @converter_base_bp.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#
import ast
import os
import requests
from flask import Flask
from flask import render_template
from werkzeug.utils import secure_filename
from blueprints.checksum import Checksum
import ast


app = Flask(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
PATH_UPLOADS = os.path.join(PATH, '../uploads')
os.makedirs(PATH_UPLOADS,  exist_ok = True)
app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'


class ConverterBase:
    def __init__(self, form, url, data, html_name, new_ep, link_label, profile_pic):
        self.form = form
        self.url = url
        self.data = data
        self.html_name = html_name
        self.new_ep = new_ep
        self.link_label = link_label
        self.profile_pic = profile_pic
        self.login_url = os.getenv('CONVERTER_URL') + os.getenv('PORT_CONVERTER') + '/login'
        self.user_credentials = {"username": os.getenv("USER_NAME"), "password": os.getenv("PASSWORD")}

    def convert_file(self):
        new_token = requests.post(self.login_url, data = self.user_credentials).json()
        new_token = new_token['token']
        headers = {'Authorization': 'Bearer ' + new_token}
        file = self.form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                 secure_filename(file.filename))
        file.save(file_path)
        checksum_value = Checksum().checksum_generator_md5(file_path)
        self.data['checksum_param'] = checksum_value
        uploaded_file = open(file_path, 'rb')
        files = {'input_file': uploaded_file}
        response = requests.post(self.url, files = files, data = self.data, headers = headers)
        uploaded_file.close()
        if response.status_code == 200:
            download_link = ast.literal_eval(response.text[:-1].strip("\""))
            download_link = download_link["download_URL"]
            return render_template(f'{self.html_name}.html', form = self.form, download_link = download_link, html_name = self.html_name, new_ep = self.new_ep, link_label = self.link_label, profile_pic = self.profile_pic)
        return render_template(f'{self.html_name}.html', form = self.form, new_ep = self.new_ep, link_label = self.link_label, profile_pic = self.profile_pic)

