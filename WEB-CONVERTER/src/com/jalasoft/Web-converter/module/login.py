# #
# # @login.py Copyright (c) 2023 Jalasoft.
# # 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# # All rights reserved.
# #
# # This software is the confidential and proprietary information of
# # Jalasoft, ("Confidential Information"). You shall not
# # disclose such Confidential Information and shall use it only in
# # accordance with the terms of the license agreement you entered into
# # with Jalasoft.
# #
#
# # Python standard libraries
# import json
# import os
# import sqlite3
# from dotenv import load_dotenv
#
# # Third party libraries
# from flask_login import (
#     LoginManager,
#     current_user,
#     login_required,
#     login_user,
#     logout_user
# )
# from oauthlib.oauth2 import WebApplicationClient
# import requests
#
# # Internal imports
# from db import init_db_command
# from user import User
# from module.user_authenticate import LoggedUser
# from flask import Blueprint, render_template, request, redirect, url_for, app
#
# # Configuration
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# GOOGLE_DISCOVERY_URL = (
#     "https://accounts.google.com/.well-known/openid-configuration"
# )
#
# load_dotenv()
#
# login_blueprint = Blueprint('login', __name__)
#
#
# class LoginManage:
#     def __init__(self, app, login_manager, client):
#         self.app = app
#         self.login_manager = login_manager
#         self.client = client
#
#     def get_google_provider_cfg(self):
#         return requests.get(GOOGLE_DISCOVERY_URL).json()
#
#     @login_blueprint.route('/login')
#     def login(self):
#         # Find out what URL to hit for Google login
#         google_provider_cfg = self.get_google_provider_cfg()
#         print(google_provider_cfg)
#         authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#
#         # Use library to construct the request for login and provide
#         # scopes that let you retrieve user's profile from Google
#         request_uri = self.client.prepare_request_uri(
#             authorization_endpoint,
#             redirect_uri=request.base_url + "/callback",
#             scope=["openid", "email", "profile"],
#         )
#         print(request_uri)
#         return redirect(request_uri)
#
#     @login_blueprint.route('/login/callback')
#     def callback_ep(self):
#         # Get authorization code Google sent back to you
#         code = request.args.get("code")
#         print(code)
#         # Find out what URL to hit to get tokens that allow you to ask for
#         # things on behalf of a user
#         google_provider_cfg = self.get_google_provider_cfg()
#         token_endpoint = google_provider_cfg["token_endpoint"]
#         # Prepare and send request to get tokens! Yay tokens!
#         token_url, headers, body = self.client.prepare_token_request(
#             token_endpoint,
#             authorization_response=request.url,
#             redirect_url=request.base_url,
#             code=code,
#         )
#         token_response = requests.post(
#             token_url,
#             headers=headers,
#             data=body,
#             auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#         )
#         print(json.dumps(token_response.json()))
#
#         # Parse the tokens!
#         self.client.parse_request_body_response(json.dumps(token_response.json()))
#
#         # Now that we have tokens (yay) let's find and hit URL
#         # from Google that gives you user's profile information,
#         # including their Google Profile Image and Email
#         userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#         uri, headers, body = self.client.add_token(userinfo_endpoint)
#         userinfo_response = requests.get(uri, headers=headers, data=body)
#         print('user info response', json.dumps(userinfo_response.json()))
#         # We want to make sure their email is verified.
#         # The user authenticated with Google, authorized our
#         # app, and now we've verified their email through Google!
#         if userinfo_response.json().get("email_verified"):
#             unique_id = userinfo_response.json()["sub"]
#             users_email = userinfo_response.json()["email"]
#             picture = userinfo_response.json()["picture"]
#             users_name = userinfo_response.json()["given_name"]
#         else:
#             return "User email not available or not verified by Google.", 400
#
#         # Create a user in our db with the information provided
#         # by Google
#         user = User(
#             id_=unique_id, name=users_name, email=users_email, profile_pic=picture
#         )
#
#         # # Doesn't exist? Add to database
#         if not User.get(unique_id):
#             User.create(unique_id, users_name, users_email, picture)
#
#         # Begin user session by logging the user in
#         login_user(user)
#         print(current_user.is_authenticated)
#
#         # Send user back to homepage
#         return redirect(url_for('home'))
#
#     @login_blueprint.route("/logout")
#     @login_required
#     def logout(self):
#         logout_user()
#         return redirect(url_for("home"))


# # ------------------------------------------------------------------------------------
# # Configuration
# GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# GOOGLE_DISCOVERY_URL = (
#     "https://accounts.google.com/.well-known/openid-configuration"
# )
#
#
# @login_manager.unauthorized_handler
# def unauthorized():
#     return render_template('need_be_logged.html', new_ep='/login', link_label='Login',
#                            profile_pic='../static/img/user.png'), 403
#
#
# # # Naive database setup
# # try:
# #     init_db_command()
# # except sqlite3.OperationalError:
# #     # Assume it's already been created
# #     pass
# #
# # # OAuth2 client setup
# # client = WebApplicationClient(GOOGLE_CLIENT_ID)
#
#
# # Flask-Login helper to retrieve a user from our db
# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)
#
#
# @app.route("/login")
# def login():
#     # Find out what URL to hit for Google login
#     google_provider_cfg = get_google_provider_cfg()
#     print(google_provider_cfg)
#     authorization_endpoint = google_provider_cfg["authorization_endpoint"]
#
#     # Use library to construct the request for login and provide
#     # scopes that let you retrieve user's profile from Google
#     request_uri = client.prepare_request_uri(
#         authorization_endpoint,
#         redirect_uri=request.base_url + "/callback",
#         scope=["openid", "email", "profile"],
#     )
#     print(request_uri)
#     return redirect(request_uri)
#
#
# @app.route("/login/callback")
# def callback():
#     # Get authorization code Google sent back to you
#     code = request.args.get("code")
#     print(code)
#     # Find out what URL to hit to get tokens that allow you to ask for
#     # things on behalf of a user
#     google_provider_cfg = get_google_provider_cfg()
#     token_endpoint = google_provider_cfg["token_endpoint"]
#     # Prepare and send request to get tokens! Yay tokens!
#     token_url, headers, body = client.prepare_token_request(
#         token_endpoint,
#         authorization_response=request.url,
#         redirect_url=request.base_url,
#         code=code,
#     )
#     token_response = requests.post(
#         token_url,
#         headers=headers,
#         data=body,
#         auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
#     )
#     print(json.dumps(token_response.json()))
#
#     # Parse the tokens!
#     client.parse_request_body_response(json.dumps(token_response.json()))
#
#     # Now that we have tokens (yay) let's find and hit URL
#     # from Google that gives you user's profile information,
#     # including their Google Profile Image and Email
#     userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
#     uri, headers, body = client.add_token(userinfo_endpoint)
#     userinfo_response = requests.get(uri, headers=headers, data=body)
#     print('user info response', json.dumps(userinfo_response.json()))
#     # We want to make sure their email is verified.
#     # The user authenticated with Google, authorized our
#     # app, and now we've verified their email through Google!
#     if userinfo_response.json().get("email_verified"):
#         unique_id = userinfo_response.json()["sub"]
#         users_email = userinfo_response.json()["email"]
#         picture = userinfo_response.json()["picture"]
#         users_name = userinfo_response.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400
#
#     # Create a user in our db with the information provided
#     # by Google
#     user = User(
#         id_=unique_id, name=users_name, email=users_email, profile_pic=picture
#     )
#
#     # # Doesn't exist? Add to database
#     if not User.get(unique_id):
#         User.create(unique_id, users_name, users_email, picture)
#
#     # Begin user session by logging the user in
#     login_user(user)
#     print(current_user.is_authenticated)
#
#     # Send user back to homepage
#     return redirect(url_for('home'))
#
#
# @app.route("/logout")
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for("home"))
#
#
# def get_google_provider_cfg():
#     return requests.get(GOOGLE_DISCOVERY_URL).json()
#
#
# # ------------------------------------------------------------------------------------
