import json, time
import requests
import hashlib
import os
from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for, send_from_directory
from random import *
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware


PICTURE_PATH = "static/images/"
ALLOWED_EXTENSIONS = {'png', "PNG", 'jpg', "JPG", 'jpeg', "JPEG", }
CHANGE_EXTENSIONS = {
    'png': 'png',
    'PNG': 'png',
    'jpg': 'jpg',
    'JPG': 'jpg',
    'jpeg': 'jpg',
    'JPEG': 'jpg'
}


app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


app.config['PICTURE_PATH'] = PICTURE_PATH
# app.add_url_rule('/uploads/<filename>', 'uploaded_file',
#                  build_only=True)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/uploads':  app.config['PICTURE_PATH']
# })


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)
@app.route('/api/upload', methods=['GET','POST'])
def upload():
    img = request.files['file']
    if img and '.' in img.filename:
        ext = img.filename.rsplit('.', 1)[1]
        if ext in ALLOWED_EXTENSIONS:
            ext = CHANGE_EXTENSIONS[ext]
            md5 = hashlib.md5(img.read()).hexdigest()
            filename = md5 + '.' + ext
            img_folder = 'dist/static/images'
            directory = os.path.join(img_folder, filename)
            if not os.path.isfile(directory):
                img.seek(0)
                img.save(directory)
            response = {
                'filename': filename
            }
            return jsonify(response)
        return {'code': 415}
    return {'code': 415}
@app.route('/api/show', methods=['GET','POST'])
def show():
    return



@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")
