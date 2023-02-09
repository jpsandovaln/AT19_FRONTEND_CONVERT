#
# @images_rotate_bp.py Copyright (c) 2023 Jalasoft.
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

image_rotate_blueprint = Blueprint('image_rotate', __name__)


@image_rotate_blueprint.route('/image_rotate', methods=['GET', "POST"])
def image_rotate():
    """Manages endpoint for image rotator"""
    user_aut = LoggedUser().is_logged()
    form = HandleInputs()
    if form.validate_on_submit():
        url = 'http://127.0.0.1:5000/imagerotate'
        data = {'output_file': form.param1.data, 'grades': form.param2.data}
        return ConverterBase(form, url, data, "image_rotate", user_aut['new_ep'], user_aut['link_label'], user_aut['profile_pic']).convert_file()
    return render_template('image_rotate.html', form=form, new_ep=user_aut['new_ep'], link_label=user_aut['link_label'], profile_pic=user_aut['profile_pic'])

    # form = Handler2()
    #
    # if form.validate_on_submit():
    #     file = form.file.data
    #     file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
    #                              secure_filename(file.filename))
    #     file.save(file_path)
    #     uploaded_file = open(file_path, 'rb')
    #     output_type = form.param1.data
    #     fps = form.param2.data
    #     url = 'http://127.0.0.1:5000/imagerotate'
    #     data = {'output_file': output_type, 'grades': fps}
    #     files = {'input_file': uploaded_file}
    #     response = requests.post(url, files = files, data = data)
    #     uploaded_file.close()
    #
    #     if response.status_code == 200:
    #         download_link = response.text[:-1].strip("\"")
    #         return render_template('image_rotate.html', form = form, download_link = download_link, output_file = output_type)
    #
    # return render_template('image_rotate.html', form = form)
    #

