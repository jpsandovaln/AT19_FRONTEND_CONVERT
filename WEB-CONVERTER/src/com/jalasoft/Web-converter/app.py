#
# @main.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import os
import sqlite3
from flask_login import (
    LoginManager,
)
from userDB.db import init_db_command
from userDB.user import User
from login.user_authenticate import LoggedUser
from flask import Flask
from flask import render_template
from blueprints.image_to_image_bp import image_to_image_blueprint
from blueprints.image_flip_bp import image_flip_blueprint
from blueprints.video_to_images_bp import video_to_images_blueprint
from blueprints.audio_to_audio_bp import audio_to_audio_blueprint
from blueprints.image_bw_bp import image_bw_blueprint
from blueprints.image_resize_bp import image_resize_blueprint
from blueprints.image_rotate_bp import image_rotate_blueprint
from blueprints.audio_increase_volume_bp import audio_increase_volume_blueprint
from blueprints.video_to_video_bp import video_to_video_blueprint
from login.login_google import login_google_blueprint, callback_blueprint, logout_blueprint

host = str(os.getenv('HOST'))
port = int(os.getenv('PORT'))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
login_manager = LoginManager()
login_manager.init_app(app)
# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

app.register_blueprint(video_to_images_blueprint)
app.register_blueprint(video_to_video_blueprint)
app.register_blueprint(image_to_image_blueprint)
app.register_blueprint(image_flip_blueprint)
app.register_blueprint(audio_to_audio_blueprint)
app.register_blueprint(image_bw_blueprint)
app.register_blueprint(image_resize_blueprint)
app.register_blueprint(image_rotate_blueprint)
app.register_blueprint(audio_increase_volume_blueprint)
app.register_blueprint(login_google_blueprint)
app.register_blueprint(callback_blueprint)
app.register_blueprint(logout_blueprint)


@login_manager.unauthorized_handler
def unauthorized():
    """Returns unathorized message"""
    return render_template('need_be_logged.html', new_ep='/login', link_label='Login',
                           profile_pic='../static/img/user.png'), 403


@login_manager.user_loader
def load_user(user_id):
    """Gets the user from DB"""
    return User.get(user_id)


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    """Manages home's page"""
    user_aut = LoggedUser().is_logged()
    return render_template('index.html', new_ep=user_aut['new_ep'], link_label=user_aut['link_label'],
                           profile_pic=user_aut['profile_pic'])


if __name__ == '__main__':
    app.run(debug=True, host = host, port=port, ssl_context="adhoc")
