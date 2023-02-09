from userDB.user import User


class GetUserInformation:
    def __init__(self, user_info_response):
        self.response = user_info_response

    def get_information(self):
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
