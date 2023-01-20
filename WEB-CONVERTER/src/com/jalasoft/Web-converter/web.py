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
MEDIA_PATH= r'D:\AT19_project\web\AT19_WEBCONVERTER\src\com\jalasoft\Web-converter\uploads'

@app.route("/", methods=['GET'])
def Display_img():
    """Displays the main page and the logo"""
    Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template("index.html", user_image=Logo,)

@app.route("/", methods=['POST'])
def videotoimage():
    """Returns the link to download the converted images"""
    Logo = os.path.join(app.config['UPLOAD_FOLDER'], 'logo.png')
    file_converter = request.files['input_file']
    output_file = request.form['output_file']
    fps=request.form['fps']
    file_name = file_converter.filename
    file_converter.save(os.path.join(app.config['UPLOAD_FOLDER2'], secure_filename(file_converter.filename)))
    path=os.path.join(MEDIA_PATH, file_name)
    params = {"output_file": output_file, "fps": fps}
    f = open(path, "rb")
    download_link = requests.post('http://localhost:5000/videotoimage/zip', params, files={"input_file": f}).text[1:-2]
    print(download_link)
    return render_template("index.html", user_image=Logo, download_link=download_link)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)