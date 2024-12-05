import json
from uuid import uuid4
from flask import Blueprint, request, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import os


from werkzeug.utils import secure_filename

import models
from db import db


UPLOAD_FOLDER = 'upload'

images_bp = Blueprint('images', __name__)
@images_bp.route('/images/upload',methods=['POST'])
@jwt_required()
def upload():
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    item_id = request.form.get('id',None)
    identity = json.loads(get_jwt_identity())
    if not item_id:
        return {'msg':'缺少id'}, 400
    username = identity['username']  # 获取当前登录用户
    item = models.LostItem.query.get(item_id)
    if not item or item.upload_user != username:
        return {'msg':'权限不够'}
    if 'image' not in request.files:
        return {'msg': '文件不存在'}
    file = request.files['image']
    if not file:
        return {'msg':'文件内容不能为空'}, 400
    filename = secure_filename('0' + file.filename)
    if not ('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
        return {'msg':'图片格式不合法'},400
    unique_filename = str(uuid4()) + '-' + str(item.id) + os.path.splitext(filename)[1]
    # 保存文件到配置的目录
    item.image_path = UPLOAD_FOLDER + '/' + unique_filename
    file.save(item.image_path)
    db.session.commit()
    return {'msg': '图片上传成功'}, 200


@images_bp.route('/images/get/<int:item_id>')
def get_image(item_id):
    item = models.LostItem.query.get(item_id)
    if not item or not item.image_path or not os.path.exists(item.image_path):
        return {'msg':'图片不存在'},400
    return send_file(item.image_path)
