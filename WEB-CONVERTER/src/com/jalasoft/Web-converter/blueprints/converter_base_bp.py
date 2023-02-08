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


app = Flask(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
PATH_UPLOADS = os.path.join(PATH, '../uploads')
app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'


class ConverterBase:
    def __init__(self, form, url, data, html_name):
        self.form = form
        self.url = url
        self.data = data
        self.html_name = html_name

    def convert_file(self):
        file = self.form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                                 secure_filename(file.filename))
        file.save(file_path)
        uploaded_file = open(file_path, 'rb')
        files = {'input_file': uploaded_file}
        response = requests.post(self.url, files = files, data = self.data)
        uploaded_file.close()
        print("before if")
        if response.status_code == 200:
            print("im here 200")
            download_link = response.text[:-1].strip("\"")
            # if response.headers['Content-Type'] == 'application/json':
            #     download_link = json.loads(download_link)
            # else:
            #     download_link = download_link[:-1].strip("\"")
            # download_link = ast.literal_eval(response.text[:-1].strip("\""))
            # download_link = download_link["download_URL"]
            print(download_link)
            return render_template(f'{self.html_name}.html', form=self.form, download_link=download_link,
                                   html_name=self.html_name)
        return render_template(f'{self.html_name}.html', form=self.form)
        #     return render_template(f'{self.html_name}.html', form = self.form, download_link = download_link, html_name = self.html_name)
        # return render_template(f'{self.html_name}.html', form = self.form)


