#
# @audio_increase_volume_bp.py Copyright (c) 2023 Jalasoft.
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
from flask_login import login_required
from blueprints.handle_inputs import HandleInputs
from blueprints.converter_base_bp import ConverterBase
from login.user_authenticate import LoggedUser
import os
from dotenv import load_dotenv
load_dotenv()

port = int(os.getenv('PORT'))
host = str(os.getenv('HOST_PRIVATE'))

audio_increase_volume_blueprint = Blueprint('audio_increase_volume', __name__)


class AudioIncreaseVolumeController:

    @audio_increase_volume_blueprint.route('/audio_increase_volume', methods = ['GET', "POST"])
    @login_required
    def audio_increase_volume():
        """Manages endpoint for video to images converter"""
        form = HandleInputs()
        user_aut = LoggedUser().is_logged()
        if form.validate_on_submit():
            url = 'http://host:port/audioincreasevolume'
            data = {'output_file': form.param1.data, 'multiplier': form.param2.data}
            return ConverterBase(form, url, data, "audio_increase_volume", user_aut['new_ep'], user_aut['link_label'], user_aut['profile_pic']).convert_file()
        return render_template('audio_increase_volume.html', form = form, new_ep=user_aut['new_ep'], link_label=user_aut['link_label'], profile_pic=user_aut['profile_pic'])


