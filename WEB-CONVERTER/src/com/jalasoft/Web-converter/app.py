#
# @app.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

# Python standard libraries
import json
import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

# Third party libraries
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

# Internal imports
from db import init_db_command
from user import User
from module.user_authenticate import LoggedUser

from flask import Flask, redirect, request, url_for
from flask import render_template
from blueprints.image_to_image_bp import image_to_image_blueprint
from blueprints.image_flip_bp import image_flip_blueprint
from blueprints.video_to_images_bp import video_to_images_blueprint
from blueprints.video_to_video_bp import video_to_video_blueprint
from blueprints.audio_to_audio_bp import audio_to_audio_blueprint
from blueprints.image_bw_bp import image_bw_blueprint
from blueprints.image_resize_bp import image_resize_blueprint
from blueprints.image_rotate_bp import image_rotate_blueprint
from blueprints.audio_increase_volume_bp import audio_increase_volume_blueprint
# from module.login import login_blueprint, LoginManage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

app.register_blueprint(video_to_images_blueprint)
app.register_blueprint(video_to_video_blueprint)
app.register_blueprint(image_to_image_blueprint)
app.register_blueprint(image_flip_blueprint)
app.register_blueprint(audio_to_audio_blueprint)
app.register_blueprint(image_bw_blueprint)
app.register_blueprint(image_resize_blueprint)
app.register_blueprint(image_rotate_blueprint)
app.register_blueprint(audio_increase_volume_blueprint)
# app.register_blueprint(login_blueprint)

@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    """Manages home's page"""
    user_aut = LoggedUser().is_logged()
    return render_template('index.html', new_ep=user_aut['new_ep'], link_label=user_aut['link_label'],
                           profile_pic=user_aut['profile_pic'])


# ------------------------------------------------------------------------------------
# Configuration
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# Flask app setup

# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template('need_be_logged.html', new_ep='/login', link_label='Login',
                           profile_pic='../static/img/user.png'), 403


# Naive database setup
try:
    init_db_command()
except sqlite3.OperationalError:
    # Assume it's already been created
    pass

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# LoginManage(app, login_manager, client)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    print(google_provider_cfg)
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(authorization_endpoint, redirect_uri=request.base_url + "/callback",
                                             scope=["openid", "email", "profile"])
    print('request uri: ', request_uri)
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    print(code)
    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    ) # this returns the "access token", "expires_in", "scope", "token_type", "id_token"
    print(json.dumps(token_response.json()))

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print('user info response', json.dumps(userinfo_response.json()))
    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = User(
        id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

    # # Doesn't exist? Add to database
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for('home'))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


# ------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True, port=5017, ssl_context="adhoc")
