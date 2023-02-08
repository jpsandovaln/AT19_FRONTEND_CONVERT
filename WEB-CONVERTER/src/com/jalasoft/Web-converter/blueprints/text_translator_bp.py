#
# @video_to_video_bp.py Copyright (c) 2023 Jalasoft.
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

text_translator_blueprint = Blueprint('text_translator', __name__)


class TextTranslatorController:

    @text_translator_blueprint.route('/text_translator', methods = ['GET', "POST"])
    def text_translator():
        """Manages endpoint for text translator"""
        form = HandleInputs()
        user_aut = LoggedUser().is_logged()
        if form.validate_on_submit():
            url = 'http://127.0.0.1:5000/texttranslator'
            data = {'output_file': form.param1.data}
            return ConverterBase(form, url, data, "video_to_video", user_aut['new_ep'], user_aut['link_label'], user_aut['profile_pic']).convert_file()
        return render_template('video_to_video.html', form = form, new_ep=user_aut['new_ep'], link_label=user_aut['link_label'], profile_pic=user_aut['profile_pic'])

