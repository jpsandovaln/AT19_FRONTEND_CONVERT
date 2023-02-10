#
# @login_google.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

import json
import os
from dotenv import load_dotenv
from flask_login import login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient
import requests
from flask import Flask, redirect, request, url_for, Blueprint
from login.user_info import GetUserInformation

app = Flask(__name__)
load_dotenv()
login_google_blueprint = Blueprint('login', __name__)
callback_blueprint = Blueprint('callback', __name__)
logout_blueprint = Blueprint('logout', __name__)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)
client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    """Gets google provider config"""
    return requests.get(GOOGLE_DISCOVERY_URL).json()


class GoogleLogin:

    @login_google_blueprint.route("/login")
    def login():
        """Manages login endpoint"""
        google_provider_cfg = get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = client.prepare_request_uri(authorization_endpoint, redirect_uri=request.base_url + "/callback",
                                                 scope=["openid", "email", "profile"])
        return redirect(request_uri)

    @callback_blueprint.route("/login/callback")
    def callback():
        """Manages callback endpoint"""
        code = request.args.get("code")
        google_provider_cfg = get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]
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
        )  # this returns the "access tokenLogin", "expires_in", "scope", "token_type", "id_token"
        client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        user = GetUserInformation(userinfo_response).get_information()
        login_user(user)
        return redirect(url_for('home'))

    @logout_blueprint.route("/logout")
    @login_required
    def logout():
        """Manages logout endpoint"""
        logout_user()
        return redirect(url_for("home"))
