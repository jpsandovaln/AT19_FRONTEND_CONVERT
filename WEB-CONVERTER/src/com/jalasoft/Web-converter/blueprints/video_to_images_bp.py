#
# @video_to_images_bp.py Copyright (c) 2023 Jalasoft.
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


video_to_images_blueprint = Blueprint('video_to_images', __name__)
load_dotenv()
CONVERTER_URL = os.getenv("CONVERTER_URL")
PORT_CONVERTER = os.getenv("PORT_CONVERTER")


class VideoToImagesController:

    @video_to_images_blueprint.route('/video_to_images', methods = ['GET', "POST"])
    def video_to_images():
        """Manages endpoint for video to images converter"""
        form = HandleInputs()
        user_aut = LoggedUser().is_logged()
        if form.validate_on_submit():
            url = CONVERTER_URL + PORT_CONVERTER + '/videotoimage/zip'
            data = {'output_file': form.param1.data, 'fps': form.param2.data}
            return ConverterBase(form, url, data, "video_to_images", user_aut['new_ep'], user_aut['link_label'], user_aut['profile_pic']).convert_file()
        return render_template('video_to_images.html', form = form, new_ep=user_aut['new_ep'], link_label=user_aut['link_label'], profile_pic=user_aut['profile_pic'])


