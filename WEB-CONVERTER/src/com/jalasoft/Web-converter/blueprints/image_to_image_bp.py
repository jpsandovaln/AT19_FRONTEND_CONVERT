#
# @image_to_image_bp.py Copyright (c) 2023 Jalasoft.
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

image_to_image_blueprint = Blueprint('image_to_image', __name__)


class ImageToImageController:

    @image_to_image_blueprint.route('/image_to_image', methods=['GET', "POST"])
    def image_to_image():
        """ Manages endpoint for image to image converter"""
        form = HandleInputs()
        if form.validate_on_submit():
            url = 'http://127.0.0.1:5000/imagetoimage'
            data = {'output_file': form.param1.data}
            return ConverterBase(form, url, data, "image_to_image").convert_file()
        return render_template('image_to_image.html', form=form)
