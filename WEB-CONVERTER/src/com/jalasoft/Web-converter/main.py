#
# @main.py Copyright (c) 2023 Jalasoft.
# 2643 Av Melchor Perez de Olguin, Colquiri Sud, Cochabamba, Bolivia.
# All rights reserved.
#
# This software is the confidential and proprietary information of
# Jalasoft, ("Confidential Information"). You shall not
# disclose such Confidential Information and shall use it only in
# accordance with the terms of the license agreement you entered into
# with Jalasoft.
#

from flask import Flask
from flask import render_template
from blueprints.image_to_image_bp import image_to_image_blueprint
from blueprints.image_flip_bp import image_flip_blueprint
from blueprints.video_to_images_bp import video_to_images_blueprint
from blueprints.video_to_video_bp import video_to_video_blueprint
from blueprints.audio_to_audio_bp import audio_to_audio_blueprint
from blueprints.image_bw_bp import image_bw_blueprint
from blueprints.image_resize_bp import image_resize_blueprint
from blueprints.image_rotate_bp import image_rotate_blueprint
from blueprints.audio_increase_volume_bp import audio_increase_volume_blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

app.register_blueprint(video_to_images_blueprint)
app.register_blueprint(video_to_video_blueprint)
app.register_blueprint(image_to_image_blueprint)
app.register_blueprint(image_flip_blueprint)
app.register_blueprint(audio_to_audio_blueprint)
app.register_blueprint(image_bw_blueprint)
app.register_blueprint(image_resize_blueprint)
app.register_blueprint(image_rotate_blueprint)
app.register_blueprint(audio_increase_volume_blueprint)


@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    """Manages home's page"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug = True, port = 5017)
