#
# @user_info.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#


from userDB.user import User


class GetUserInformation:
    """Defines Get user Information"""
    def __init__(self, user_info_response):
        self.response = user_info_response

    def get_information(self):
        """Gets the user information"""
        if self.response.json().get("email_verified"):
            unique_id = self.response.json()["sub"]
            users_email = self.response.json()["email"]
            picture = self.response.json()["picture"]
            users_name = self.response.json()["given_name"]
        else:
            return "User email not available or not verified by Google.", 400
        user = User(
            id_=unique_id, name=users_name, email=users_email, profile_pic=picture
        )
        if not User.get(unique_id):
            User.create(unique_id, users_name, users_email, picture)

        return user
