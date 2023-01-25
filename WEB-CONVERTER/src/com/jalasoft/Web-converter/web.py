from ast import literal_eval

from flask import Flask
from flask import request
from flask import render_template
from werkzeug.utils import secure_filename
from pathlib import Path
import os
import requests

app = Flask(__name__)

img_folder = os.path.join('static', 'IMG')
app.config['UPLOAD_FOLDER'] = img_folder
input_folder = os.path.join('uploads')
app.config['UPLOAD_FOLDER2'] = input_folder
# MEDIA_PATH = r'D:\AT19_project\web\AT19_WEBCONVERTER\src\com\jalasoft\Web-converter\uploads'
MEDIA_PATH = os.path.realpath(os.path.dirname(__file__))
MEDIA_PATH = os.path.join(MEDIA_PATH, 'uploads')


@app.route("/", methods=['GET'])
def display_img():
    """Displays the main page and the logo"""
    logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template("index2.html", user_image=logo)


# @app.route("/", methods=['POST'])
# def videotoimage(request):
#     """Returns the link to download the converted images"""
#     logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
#     file_converter = request.files['input_file']
#     output_file = request.form['output_file']
#     fps = request.form['fps']
#     file_name = file_converter.filename
#     file_converter.save(os.path.join(app.config['UPLOAD_FOLDER2'], secure_filename(file_converter.filename)))
#     path = os.path.join(MEDIA_PATH, file_name)
#     params = {"output_file": output_file, "fps": fps}
#     f = open(path, "rb")
#     download_link = requests.post('http://localhost:5000/videotoimage/zip', params, files={"input_file": f}).text[1:-2]
#     print(download_link)
#     return render_template("index2.html", user_image=logo, download_link=download_link)

@app.route("/", methods=['POST'])
def videotoimage(request):
        url_converter = "http://localhost:5000/videotoimage/zip"
        file_converter = request.files['input_file']
        filename = secure_filename(file_converter.filename)
        file_converter.save(os.path.join(MEDIA_PATH, filename))
        uploaded_file_converter = open(file_converter, 'rb')

        output_file = request.form['output_file']
        fps = request.form['fps']

        files = {
            'input_file': uploaded_file_converter
        }
        parameters = {
            'output_file': output_file,
            'fps': fps
        }

        r = requests.post(url_converter, params=parameters, files=files)
        r = r.content.decode('utf-8')
        r = literal_eval(r)
        print(r)
        return render_template('index2.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)