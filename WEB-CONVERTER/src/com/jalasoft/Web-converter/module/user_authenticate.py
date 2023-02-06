from flask_login import current_user


class LoggedUser:
    def is_logged(self):
        if current_user.is_authenticated:
            new_ep = '/logout'
            link_label = 'Logout'
            profile_pic = current_user.profile_pic
            return {'new_ep': new_ep, 'link_label': link_label, 'profile_pic': profile_pic}
        else:
            new_ep = '/login'
            link_label = 'Login'
            profile_pic = '../static/img/user.png'
            return {'new_ep': new_ep, 'link_label': link_label, 'profile_pic': profile_pic}
