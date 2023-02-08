#
# @image_flip_bp.py Copyright (c) 2023 Jalasoft.
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

image_flip_blueprint = Blueprint('image_flip', __name__)


class ImageFlipController:

    @image_flip_blueprint.route('/image_flip', methods=['GET', "POST"])
    def image_flip():
        """Manages endpoint for image flipper"""
        form = HandleInputs()
        if form.validate_on_submit():
            url = 'http://127.0.0.1:5000/imageflip'
            data = {'output_file': form.param1.data}
            return ConverterBase(form, url, data, "image_flip").convert_file()
        return render_template('image_flip.html', form=form)


