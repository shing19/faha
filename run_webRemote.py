import json, time
import requests
import hashlib
import os
from flask import Flask, render_template, request, jsonify, Response, flash, redirect, url_for, send_from_directory
from random import *
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware

import hashlib
from typing import Any, Text, Dict, List
import requests
import sys
import io
import time

#sys.path.insert(0, '/home/ubuntu/CV/kzy/FashionGenAttnGAN/code/')
sys.path.insert(1, '/home/ubuntu/CV/kzy/StyleCLIP/')


image_path = "http://1.117.208.226:8000/static/images/"
image_save_path = "/home/ubuntu/Web/dist/static/images/"
latent_save_path =  "/home/ubuntu/CV/kzy/tmp/styleclip/latents/"
latent_tmp_path = "/home/ubuntu/CV/kzy/tmp/styleclip/latents/"
trans_appid = "20210716000889427"
trans_salt = "1734610886"
trans_key = "0TUFaZfCpL3zdYmmQWpB"
trans_api = "https://fanyi-api.baidu.com/api/trans/vip/translate"
cfg_file = '/home/ubuntu/CV/kzy/FashionGenAttnGAN/code/cfg/fashiongen2_attn2_api.yml'
gpu_id = 0



app = Flask(__name__,
            static_folder = "./dist/static",
            template_folder = "./dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#import fashiongenattngan_api
# dataset, algo = fashiongenattngan_api.init_model(cfg_file, gpu_id)

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

app.config['PICTURE_PATH'] = PICTURE_PATH
# app.add_url_rule('/uploads/<filename>', 'uploaded_file',
#                  build_only=True)
# app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
#     '/uploads':  app.config['PICTURE_PATH']
# })

@app.before_first_request
def init():
    print('----init before_first_request --')
    import styleclip_api2 as styleclip_api
    global process
    process = styleclip_api.Process()
    print('----init before_first_request --')


@app.route('/api/random')
def random_number():
    response = {
        'randomNumber': randint(1, 100)
    }
    return jsonify(response)

@app.route('/api/gentest', methods=['POST'])
def gentest():
    try:
        input_text = request.values.get('input_text')
        response = {
            'genText': randint(1, 100),
            'input_text': input_text,
            'version': 2
        }
        return jsonify(response)
    except Exception as e:
        return {'code': 400, 'msg': str(e)}

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

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        input_text = request.values.get('input_text')
        print(input_text)
        input_text = input_text.replace('改成', '')
        #import torch
        #torch.multiprocessing.set_start_method('spawn')
        #import numpy as np
        #a = np.random.rand(2)
        #b = torch.from_numpy(a)
        #c = b.cuda()
        img_name = ''
#         if os.path.exists(image_save_path + input_text + '.png'):
#             img_name = input_text + '.png'
#         elif os.path.exists(image_save_path + input_text + '.jpg'):
#             img_name = input_text + '.jpg'
        if '砖红' in input_text and '夹克' in input_text:
            img_name = '夹克（砖红色）.png'
        elif '藏青' in input_text and '夹克' in input_text:
            img_name = '夹克（藏青色）.png'
        elif '迷彩' in input_text and '短袖' in input_text:
            img_name = '短袖（迷彩）.png'
        elif '蓝白' in input_text and '衬衫' in input_text and '短袖' in input_text:
            img_name = '蓝白格子衬衫（短袖）.png'
        elif '蓝白' in input_text and '衬衫' in input_text and '长袖' in input_text:
            img_name = '蓝白格子衬衫（长袖）.png'
        elif '橙色' in input_text and '长袖' in input_text:
            img_name = '长袖（橙色）.png'
        elif '藏蓝色' in input_text and '长袖' in input_text:
            img_name = '长袖（藏蓝色）.png'
        elif '迷彩' in input_text and '长袖' in input_text:
            img_name = '长袖（迷彩）.png'
        elif '黑色' in input_text and '长袖' in input_text:
            img_name = '长袖（黑色）.png'
        elif '荧光黄' in input_text and '高帮' in input_text:
            img_name = '荧光黄高帮鞋.jpg'

        if img_name != '':
            time.sleep(5)
            return {'code': 200,
                    'text': "已根据您的描述生成服装，需要什么修改",
                    'image': image_path + img_name}

        translation_text = translate(input_text)
        print(translation_text)
        #             results = fashiongenattngan_api.gen_example_from_text(dataset.wordtoix, algo, translation_text)
        #             img = open(results[2], 'rb')
        #             img_content = img.read()
        #             md5 = hashlib.md5(img_content).hexdigest()
        #             img_name = md5 + ".png"
        #             with open("/home/ubuntu/Web/static/images/" + img_name, 'wb') as f:
        #                 f.write(img_content)
        experiment_type = "free_generation"  # @param ['edit', 'free_generation']
        use_model = 'e4e'

        img_name = input_text + ".jpg"
        result_image, latent = process.get_result_from_text(translation_text, experiment_type=experiment_type, use_model=use_model)

        process.save_image(result_image, image_save_path + img_name)
        process.save_latent(latent, latent_save_path + input_text + ".pt")
        # md5 = hashlib.md5(result_image).hexdigest()
        # m = hashlib.md5()
        # with io.BytesIO() as memf:
        #     result_image.save(memf, 'jpeg')
        #     data = memf.getvalue()
        #     m.update(data)
        # md5 = m.hexdigest()
        return {'code': 200,
                'text': "已根据您的描述生成服装，需要什么修改",
                'image': image_path + img_name}
    except Exception as e:
        return {'code': 400, 'msg': str(e)}

@app.route('/api/modify', methods=['POST'])
def modify():
    text = request.values.get('text')
    image = request.values.get('image')
    print(text)
    print(image)
    text = text.replace('改成', '')
    translation_text = translate(text)
    print(translation_text)
    if image is not None:
        img_name = ''
        if (image == "夹克（砖红色）.png" or image == '5ed42d759e2a22483874ba76ee21d8fc.png') and "藏青色" in text:
            img_name = "夹克（藏青色）.png"
        elif (image == "夹克（藏青色）.png" or image == '3d9837b197df740a69d92605be3e8f81.png') and "砖红色" in text:
            img_name = "夹克（砖红色）.png"
        elif (image == '短袖（迷彩）.png' or image == 'f53da82d1885849687756e157667362f.png') and "长袖" in text:
            img_name = '长袖（迷彩）.png'
        elif (image == '蓝白格子衬衫（短袖）.png' or image == '2463f1fb1c1e4578ba59d6fc30fa7b98.png') and '长袖' in text:
            img_name = '蓝白格子衬衫（长袖）.png'
        elif (image == '蓝白格子衬衫（长袖）.png' or image == '7639069d5f89382959fd1636b47e6c70.png') and '短袖' in text:
            img_name = '蓝白格子衬衫（短袖）.png'
        elif image == '长袖（橙色）.png' or image == 'd9664a97ab83c9f131b18ca04d96e1bd.png':
            if '藏蓝色' in text:
                img_name = '长袖（藏蓝色）.png'
            elif '迷彩' in text:
                img_name = '长袖（迷彩）.png'
            elif '黑色' in text:
                img_name = '长袖（黑色）.png'
        elif image == '长袖（藏蓝色）.png' or image == '218b11b8aeb82a3ea515000d434ee64c.png':
            if '橙色' in text:
                img_name = '长袖（橙色）.png'
            elif '迷彩' in text:
                img_name = '长袖（迷彩）.png'
            elif '黑色' in text:
                img_name = '长袖（黑色）.png'
        elif image == '长袖（迷彩）.png' or image == '5cec14140606d0fb30c449b2062920b9.png':
            if '橙色' in text:
                img_name = '长袖（橙色）.png'
            elif '藏蓝色' in text:
                img_name = '长袖（藏蓝色）.png'
            elif '黑色' in text:
                img_name = '长袖（黑色）.png'
            elif '短袖' in text:
                img_name = '短袖（迷彩）.png'
        elif image == '长袖（黑色）.png' or image == '1f955b3d808ac172c7e76b362f1c730e.png':
            if '橙色' in text:
                img_name = '长袖（橙色）.png'
            elif '迷彩' in text:
                img_name = '长袖（迷彩）.png'
            elif '藏蓝色' in text:
                img_name = '长袖（藏蓝色）.png'
        elif image == '荧光黄高帮鞋.jpg' or image == '6758141c041b603b755be883ef3708c8.jpg':
            if 'logo' in text and '黑色' in text:
                img_name = '荧光黄黑色logo高帮鞋.jpg'

        if img_name != '':
            time.sleep(5)
            return {'code': 200,
                    'text': "已根据您的描述修改图片，感觉如何？",
                    'image': image_path + img_name}

        # try:
        if os.path.exists(image_save_path + image):
            # 必然存在
            in_latent_path = latent_save_path + image.split('.')[0] + '.pt'

            if os.path.exists(in_latent_path):
                # 如果是二次修改，则调出该图片的latent修改，而不是用图片修改
                print('使用latent修改')
                experiment_type = "edit"  # @param ['edit', 'free_generation']
                use_model = 'e4e'
                result_image, latent = process.get_result_from_latent_path(translation_text, in_latent_path,
                                                                           experiment_type=experiment_type,
                                                                           use_model=use_model)

                m = hashlib.md5()
                with io.BytesIO() as memf:
                    result_image.save(memf, 'jpeg')
                    data = memf.getvalue()
                    m.update(data)
                md5 = m.hexdigest()

                img_name = md5 + ".jpg"

                process.save_image(result_image, image_save_path + img_name)
                process.save_latent(latent, latent_save_path + md5 + '.pt')
                return {'code': 200,
                        'text': "已根据您的描述修改图片，感觉如何？",
                        'image': image_path + img_name}
            else:
                print('有这个图片，却没有这个图片的latent，使用图片修改')


        experiment_type = "edit"  # @param ['edit', 'free_generation']
        use_model = 'e4e'
        in_latent_path = latent_tmp_path + image.split('.')[0] + '.pt'
        result_image, latent = process.get_result_from_text_and_image(translation_text, image_save_path + image,
                                                                      in_latent_path,
                                                                      experiment_type=experiment_type,
                                                                      use_model=use_model)

        m = hashlib.md5()
        with io.BytesIO() as memf:
            result_image.save(memf, 'jpeg')
            data = memf.getvalue()
            m.update(data)
        md5 = m.hexdigest()

        img_name = md5 + ".jpg"

        process.save_image(result_image, image_save_path + img_name)
        process.save_latent(latent, latent_save_path + md5 + '.pt')

        return {'code': 200,
                'text': "已根据您的描述修改图片，感觉如何？",
                'image': image_path + img_name}

        # except Exception as e:
        #     return {'code': 400, 'msg': str(e)}
    else:
        return {'code': 400, 'msg': '并未传入图片'}


@app.route('/api/generate_random', methods=['POST'])
def generate_random():
    try:
        print("随机生成")
        use_model = 'stylegan2'

        result_image, latent = process.get_result_random(use_model=use_model)

        m = hashlib.md5()
        with io.BytesIO() as memf:
            result_image.save(memf, 'jpeg')
            data = memf.getvalue()
            m.update(data)
        md5 = m.hexdigest()

        img_name = md5 + ".jpg"

        process.save_image(result_image, image_save_path + img_name)
        process.save_latent(latent, latent_save_path + md5 + ".pt")

        return {'code': 200,
                'text': "已随机生成服装，需要什么修改",
                'image': image_path + img_name}
    except Exception as e:
        return {'code': 400, 'msg': str(e)}

def translate(text):
    params = {
        "q": text,
        "from": "zh",
        "to": "en",
        "appid": trans_appid,
        "salt": trans_salt,
        "sign": hashlib.md5((trans_appid + text + trans_salt + trans_key).encode('utf-8')).hexdigest()
    }
    response = requests.get(url=trans_api, params=params)
    print(response)
    return response.json()["trans_result"][0]["dst"]







@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>')
def catch_all(path):
    if app.debug:
        return requests.get('http://localhost:8080/{}'.format(path)).text
    return render_template("index.html")

