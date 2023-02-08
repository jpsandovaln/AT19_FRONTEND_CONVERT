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

video_to_images_blueprint = Blueprint('video_to_images', __name__)


class VideoToImagesController:

    @video_to_images_blueprint.route('/video_to_images', methods = ['GET', "POST"])
    def video_to_images():
        """Manages endpoint for video to images converter"""
        form = HandleInputs()
        if form.validate_on_submit():
            url = 'http://127.0.0.1:5000/videotoimage/zip'
            data = {'output_file': form.param1.data, 'fps': form.param2.data}
            return ConverterBase(form, url, data, "video_to_images").convert_file()
        return render_template('video_to_images.html', form = form)


