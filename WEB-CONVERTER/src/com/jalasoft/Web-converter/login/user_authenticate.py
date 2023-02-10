#
# @user_authenticate.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask_login import current_user


class LoggedUser:
    """Defines Logged User"""
    def is_logged(self):
        """Verifies if the user is authenticated"""
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
