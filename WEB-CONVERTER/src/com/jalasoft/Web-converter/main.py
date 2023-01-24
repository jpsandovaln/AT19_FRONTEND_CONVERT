from flask import Flask
from flask import render_template
from flask import request
import requests

import os

app = Flask(__name__)

PATH = os.path.realpath(os.path.dirname(__file__))
PATH_LOGO = os.path.join(PATH, 'static', 'img', 'logo.png')


@app.route('/')
def principal():
    return render_template('index.html')


@app.route('/', methods=['GET'])
def display_img():
    """Displays the main page and the logo"""

    return render_template("index.html")


@app.route('/video')
def video():
    misLenguajes = ("PHP", "Python", "Java", "C#",
                    "JavaScript", "Perl", "Ruby", "Rust")
    return render_template('video.html', lenguajes=misLenguajes)


@app.route('/contacto')
def contacto():
    return render_template('contacto.html')


if __name__ == '__main__':
    app.run(debug=True, port=5017)