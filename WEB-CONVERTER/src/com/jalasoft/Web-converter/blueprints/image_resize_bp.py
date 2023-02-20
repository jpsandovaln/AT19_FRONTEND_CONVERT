#
# @image_resize_bp.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask import Blueprint
from flask import render_template
from blueprints.handle_inputs import HandleInputs
from blueprints.converter_base_bp import ConverterBase
from login.user_authenticate import LoggedUser
from dotenv import load_dotenv
import os

image_resize_blueprint = Blueprint('image_resize', __name__)
load_dotenv()
CONVERTER_URL = os.getenv("CONVERTER_URL")
PORT_CONVERTER = os.getenv("PORT_CONVERTER")


class ImageResizeController:

    @image_resize_blueprint.route('/image_resize', methods=['GET', "POST"])
    def image_resize():
        """Manages endpoint for image resizer"""
        form = HandleInputs()
        user_aut = LoggedUser().is_logged()
        if form.validate_on_submit():
            url = CONVERTER_URL + PORT_CONVERTER + '/imageresize'
            data = {'output_file': form.param1.data, 'new_size': form.param2.data}
            return ConverterBase(form, url, data, "image_resize", user_aut['new_ep'], user_aut['link_label'], user_aut['profile_pic']).convert_file()
        return render_template('image_resize.html', form=form, new_ep=user_aut['new_ep'], link_label=user_aut['link_label'], profile_pic=user_aut['profile_pic'])

