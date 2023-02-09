#
# @audio_to_audio_bp.py Copyright (c) 2023 Jalasoft.
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


audio_to_audio_blueprint = Blueprint('audio_to_audio', __name__)


class AudioToAudioController:

    @audio_to_audio_blueprint.route('/audio_to_audio', methods = ['GET', "POST"])
    def audio_to_audio():
        """Manages endpoint for video to images converter"""
        form = HandleInputs()
        user_aut = LoggedUser().is_logged()
        if form.validate_on_submit():
            url = 'http://127.0.0.1:5000/audiotoaudio'
            data = {'output_file': form.param1.data}
            return ConverterBase(form, url, data, "audio_to_audio", user_aut['new_ep'], user_aut['link_label'], user_aut['profile_pic']).convert_file()
        return render_template('audio_to_audio.html', form = form, new_ep=user_aut['new_ep'], link_label=user_aut['link_label'], profile_pic=user_aut['profile_pic'])



#
#
# @audio_to_audio_blueprint.route('/audio_to_audio', methods = ['GET', "POST"])
# def audio_to_audio():
#     """Manages endpoint for audio to audio converter"""
#     form = Handler1()
#
#     if form.validate_on_submit():
#
#         file = form.file.data
#         file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
#                                  secure_filename(file.filename))
#         file.save(file_path)
#         uploaded_file = open(file_path, 'rb')
#         output_type = form.param1.data
#         url = 'http://127.0.0.1:5000/audiotoaudio'
#         data = {'output_file': output_type}
#         files = {'input_file': uploaded_file}
#         response = requests.post(url, files = files, data = data)
#         uploaded_file.close()
#
#         if response.status_code == 200:
#             download_link = response.text[:-1].strip("\"")
#             return render_template('audio_to_audio.html', form = form, download_link = download_link)
#
#     return render_template('audio_to_audio.html', form = form)
