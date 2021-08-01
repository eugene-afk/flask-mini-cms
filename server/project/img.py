import os
import uuid
import pathlib
from flask import Blueprint, redirect, request, url_for, flash, Markup, jsonify
from flask_login import login_required
from os.path import join, dirname, realpath
from . import db, csrf
from .models import Media, Post
from datetime import datetime
from PIL import Image

img = Blueprint('img', __name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'gif', 'png', 'webp'}
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/img/media') 
ROW_PER_PAGE = 10

@img.route('/dimg/<id>', methods=['GET','POST'])
@login_required
def dimg(id):
    try:
        img = Media.query.filter_by(id=id).first()
        name = img.media_name
        posts = Post.query.filter_by(imgMain=name).all()
        for i in posts:
            i.imgMain = 'default.jpg'

        db.session.delete(img)
        db.session.commit()

        os.remove(os.path.join(UPLOAD_FOLDER, name))
        os.remove(os.path.join(UPLOAD_FOLDER, name.replace('.webp', img.original_extension)))

        flash(Markup('Image <strong>' + str(name) + '</strong> was deleted! For posts using this image ' + 
                    'has been changed to default '))
        flash('success')
        return redirect(url_for('main.images'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** dimg msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))

@img.route('/saveimg', methods=['POST'])
@login_required
# @csrf.exempt
def save_img_post():
    try:
        newImageName = save_img(request.files)
    except:
        return ''
    if newImageName != '':
        return '/static/img/media/' + newImageName
    return ''

@img.route('/saveimgf', methods=['POST'])
@login_required
def save_img_postf():
    try:
        newImageName = save_img(request.files)
        flash(Markup('Image saved! filename: <strong>' + newImageName + '</strong>'))
        flash('success')
        return redirect(url_for('main.images'))
    except Exception as ex:
        print('*** ' + str(datetime.now()) + ' *** save_img_postf msg: ' + str(ex))
        return redirect(url_for('errors.unknownerror'))


@img.route('/imglist', methods=['GET'])
@login_required
def imglist():
    try:
        page = request.args.get('page', 1, type=int)
        imgs = Media.query.paginate(page=page, per_page=ROW_PER_PAGE)
        data = {
            'total_pages': imgs.pages,
            'current_page': imgs.page,
            'imgs':
                [e.serialize() for e in imgs.items]
        }
    except Exception as ex:
        data = {
        'error': str(ex),
        }
    return jsonify(data)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_img(files):
    if 'img' not in files:
        return ''
    img = files['img']
    if img.filename == '':
        return ''
    if img and allowed_file(img.filename):
        extension = pathlib.Path(img.filename).suffix
        newImageName = uuid.uuid4().hex + extension

        path = os.path.join(UPLOAD_FOLDER, newImageName)
        img.save(path)

        newImageName_converted = newImageName.replace(extension, '.webp')
        media_itm = Media.query.filter_by(media_name=newImageName_converted).first()

        if not media_itm:
            media_itm = Media(media_name=newImageName_converted, original_extension=extension, pure_name=newImageName.replace(extension, ''))
            db.session.add(media_itm)
            db.session.commit()

            try: 
                image = Image.open(path)
                image = image.convert('RGB')
                image.save(path.replace(extension, '.webp'), 'webp')
            except Exception as ex:
                print('*** ' + str(datetime.now()) + ' *** save_img msg: ' + str(ex))
                return newImageName

        return newImageName_converted
