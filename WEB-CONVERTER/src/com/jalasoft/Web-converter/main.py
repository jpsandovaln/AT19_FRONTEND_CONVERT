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
# from blueprints import video_bp, image_bp
from blueprints.image_to_image_blueprint import image_blueprint
from blueprints.image_flip_blueprint import image_flip_blueprint
from blueprints.video_blueprint import video_blueprint

app = Flask(__name__)
# PATH = os.path.realpath(os.path.dirname(__file__))
# PATH_UPLOADS = os.path.join(PATH, 'uploads')
# app.config['UPLOAD_FOLDER'] = PATH_UPLOADS
app.config['SECRET_KEY'] = 'supersecretkey'
app.register_blueprint(video_blueprint)
app.register_blueprint(image_blueprint)
app.register_blueprint(image_flip_blueprint)

#
@app.route('/', methods=['GET', "POST"])
@app.route('/home', methods=['GET', "POST"])
def home():
    return render_template('index.html')


# @app.route('/video', methods=['GET', "POST"])
# def video():
    # form = UploadVideo()
    #
    # if form.validate_on_submit():
    #
    #     file = form.file_video.data
    #     file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
    #                              secure_filename(file.filename))
    #     file.save(file_path)
    #     uploaded_file = open(file_path, 'rb')
    #     output_type = form.param1_video.data
    #     fps = form.param2_video.data
    #     url = 'http://127.0.0.1:5000/videotoimage/zip'
    #     data = {'output_file': output_type, 'fps': fps}
    #     files = {'input_file': uploaded_file}
    #     response = requests.post(url, files=files, data=data)
    #     uploaded_file.close()
    #     print(response)
    #     if response.status_code == 200:
    #         download_link = response.text[:-1].strip("\"")
    #         return render_template('video.html', form=form, download_link=download_link, output_file = output_type)
    #     else:
    #         return "Sorry video"
    # return render_template('video.html', form=form)

#
# @app.route('/image', methods=['GET', "POST"])
# def image():
#     form = UploadImage()
#
#     if form.validate_on_submit():
#
#         file = form.file_image.data
#         file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
#                                  secure_filename(file.filename))
#         file.save(file_path)
#         uploaded_file = open(file_path, 'rb')
#         output_type = form.param1_image.data
#         # aux = form.param2.data
#         url = 'http://127.0.0.1:5000/imagetoimage'
#         data = {'output_file': output_type}
#         files = {'input_file': uploaded_file}
#         response = requests.post(url, files=files, data=data)
#         uploaded_file.close()
#
#         if response.status_code == 200:
#             download_link = response.text[:-1].strip("\"")
#             return render_template('image.html', form=form, download_link=download_link)
#         else:
#             return "Sorry"
#     return render_template('image.html', form=form)
#

if __name__ == '__main__':
    app.run(debug=True, port=5017)
