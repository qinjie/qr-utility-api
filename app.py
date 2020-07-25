
from flask import Flask, request, send_from_directory, jsonify
import qrcode
from pyzbar import pyzbar
from PIL import Image
from datetime import datetime
import os

app = Flask(__name__)

def gen_qr(data, output_file=''):
    img = qrcode.make(data)
    if output_file:
        img.save(output_file)
    return img

def resize_image(img, maxwidth=256, maxheight=256, output_file=''):
    width, height = img.size 
    ratio = min(maxwidth/width, maxheight/height)
    newimg = img.resize((int(width*ratio), int(height*ratio)))
    if output_file:
        img.save(output_file)
    return newimg

def stack_images(back_img, front_img, position, output_file=''):
    new_img = back_img.copy()
    new_img.paste(front_img, position)
    if output_file:
        new_img.save(output_file)
    return new_img


def get_time_string():
    '''Return a string representation of time including hours, minutes, seconds and milliseconds.
    This is used as file name.'''
    t = datetime.now()
    return t.strftime('%H%M%S%f')


# Data is included in path
@app.route('/qr_code/<string:data>', methods=['GET'])
def qr_get(data):
    output_file = '{0}.png'.format(get_time_string())
    folder = 'static'
    gen_qr(data,  os.path.join(folder, output_file))
    return send_from_directory(folder, output_file)


# Data is posted as raw
@app.route('/qr_code', methods=['POST'])
def qr_post():
    data = request.data
    output_file = '{0}.png'.format(get_time_string())
    folder = 'static'
    gen_qr(data, os.path.join(folder, output_file))
    return send_from_directory(folder, output_file)


# Logo image are posted by multipart with name = 'image'
@app.route('/qr_with_logo', methods=['POST'])
def qr_with_logo():
    width = request.args.get('width', '64')
    logo_width = int(width)

    # request.files is a dictionary
    file = request.files.get('logo', None)
    if not file:
        return 'Must upload file as multipart with name "logo"', 400
    img_logo = Image.open(file)
    print(img_logo.width, img_logo.height)
    
    data = request.form.get('data', None)
    if not data:
        return 'Missing data "data" for QR Code', 400

    img_qr = gen_qr(data)
    # So that logo will be color instead of graysale
    img_qr_rgb = img_qr.convert('RGB')
    # resize logo image
    img_small = resize_image(img_logo, maxwidth=logo_width)
    # position in the middle of background image
    pos = ((img_qr_rgb.size[0] - img_small.size[0]) // 2, (img_qr_rgb.size[1] - img_small.size[1]) // 2)

    output_file = '{0}.png'.format(get_time_string())
    folder = 'static'
    stack_images(img_qr_rgb, img_small, pos, os.path.join(folder, output_file))
    return send_from_directory(folder, output_file)


@app.route('/qr_in_image', methods=['POST'])
def qr_in_image():
    frac = request.args.get('fraction', '0.2')
    qr_width_fraction = float(frac)

    file = request.files.get('image', None)
    if not file:
        return 'Must upload file as multipart with name "image"', 400
    img_bg = Image.open(file)

    data = request.form.get('data', None)
    if not data:
        return 'Missing data "data" for QR Code', 400
    print(data)

    img_qr = gen_qr(data)
    qr_max_width = int(img_bg.width * qr_width_fraction)
    img_small = resize_image(img_qr, qr_max_width)
    # position at the bottom right corner of the image
    pos = (img_bg.size[0] - img_small.size[0], img_bg.size[1] - img_small.size[1])

    output_file = '{0}.png'.format(get_time_string())
    folder = 'static'
    stack_images(img_bg, img_small, pos, os.path.join(folder, output_file))
    return send_from_directory(folder, output_file)

@app.route('/qr_decode', methods=['POST'])
def qr_decode():
    '''
    Able to decode multiple QR codes in the image. Return data includes position of QR codes.
    '''
    file = request.files.get('image', None)
    if not file:
        return 'Must upload file as multipart with name "image"', 400

    img = Image.open(file)
    qrcodes = pyzbar.decode(img)
    print(len(qrcodes))

    result = []
    for qrcode in qrcodes:
        type = qrcode.type
        x, y, w, h = qrcode.rect
        data = qrcode.data.decode('utf-8')
        result.append({'type': type, 'data': data, 'rect': (x, y, w, h)})

    print(result)
    return jsonify(result)


app.run(port=3000, debug=True)

