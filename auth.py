import json

from flask import request, jsonify, Blueprint
from db import db
import models
from sqlalchemy import or_
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies

auth_bp = Blueprint('auth', __name__)

# 登录路由
@auth_bp.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return jsonify({"msg": "缺少参数"}), 400

    # 从数据库中获取用户（在实际应用中，你会查询数据库）
    user = models.User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity= json.dumps({'username':username,'role':user.role}))
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({"msg": "用户名或密码错误"}), 401


# 受保护的路由示例
@auth_bp.route('/user/info', methods=['GET'])
@jwt_required()
def getUserInfo():
    try:
        identity = json.loads(get_jwt_identity())
        return {'name':identity['username'], 'avatar':'avatar','roles':[identity['role']]}, 200
    except Exception as e:
        return jsonify({"msg":'无法获取用户信息'}), 401
@auth_bp.route('/user/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "成功登出"})
    unset_jwt_cookies(response)
    return response, 200

@auth_bp.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)
    checkpassword = data.get('checkpassword', None)
    if not username or not email or not password or not checkpassword:
        return jsonify({"msg": "缺少参数"}), 400

    user = models.User.query.filter_by(username=username).first()
    if user:
        return {'msg':'用户名已存在'},400
    user = models.User.query.filter_by(username=email).first()
    if user:
        return {'msg':'邮箱已注册'},400
    if password != checkpassword:
        return {'msg': '两次密码不相同'}, 400
    try:
        new_user = models.User(username=username, email=email, password=password, role='editor')
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'msg': '注册失败'}, 400
    return {'msg':'注册成功'},200



