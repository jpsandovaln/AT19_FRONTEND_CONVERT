from ast import literal_eval
from flask import Flask
from flask import render_template
from flask import request
import requests
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm, Form
from wtforms.validators import InputRequired, DataRequired
from wtforms import FileField, SubmitField, StringField
import os

app = Flask(__name__)
PATH = os.path.realpath(os.path.dirname(__file__))
PATH_UPLOADS = os.path.join(PATH, 'uploads')
app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'


class UploadFile(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    output_type = StringField("Output_type", validators=[InputRequired()])
    fps = StringField("Fps", validators=[InputRequired()])
    submit = SubmitField("Upload File")


@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    return render_template('index.html')


@app.route('/video', methods=['GET',"POST"])
def video():
    form = UploadFile()

    if form.validate_on_submit():

        file = form.file.data
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                               secure_filename(file.filename))
        file.save(file_path)
        uploaded_file = open(file_path, 'rb')
        output_type = form.output_type.data
        fps = form.fps.data

        url = 'http://127.0.0.1:5000//videotoimage/zip'

        data = {'output_file': output_type, 'fps': fps}
        files = {'input_file': uploaded_file}
        response = requests.post(url, files=files, data=data)
        print(response)
        if response.status_code == 200:
            download_link = response.text[:-1].strip("\"")
            print(download_link)
            return render_template('video.html', form=form, download_link=download_link, output_file = output_type)
        else:
            return "Sorry"
    return render_template('video.html', form=form)


if __name__ == '__main__':
    app.run(debug=True, port=5017)
