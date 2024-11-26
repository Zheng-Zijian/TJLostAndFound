import json
import random
import re
import string

from Demos.win32ts_logoff_disconnected import session
from flask import request, jsonify, Blueprint
from flask_mail import Mail, Message, current_app
import datetime

from fontTools.misc.cython import returns

from db import db
import models
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

#发送验证码
@auth_bp.route('/user/verify', methods=['POST'])
def verify():
    data = request.get_json()
    username = data.get('username', None)
    email = data.get('email', None)
    if not username or not email:
        return jsonify({"msg": "缺少参数"}), 400
    if re.match('^\w{3,50}$', username) is None:
        return jsonify({"msg": "用户名格式错误"}), 400
    if re.match('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) is None:
        return jsonify({"msg": "邮箱格式错误"}), 400
    user = models.User.query.filter_by(username=username).first()
    if user:
        return {'msg':'用户名已存在'},400
    user = models.User.query.filter_by(email=email).first()
    if user:
        return {'msg':'邮箱已注册'},400
    models.VerifyCode.query.filter(models.VerifyCode.expiration_time < datetime.datetime.now()).delete()
    db.session.commit()
    dbverifycode = models.VerifyCode.query.filter(models.VerifyCode.username==username and models.VerifyCode.email==email).first()

    if dbverifycode:
        if dbverifycode.email == email and dbverifycode.username == username:
            delta = dbverifycode.expiration_time - datetime.datetime.now()
            return {'msg':f'验证码已发送，如需重新发送，请等待{delta.seconds}秒再试'},400
        else:
            return {'msg':'该用户名或邮箱正在被其它用户注册'},400
    all_characters = string.ascii_letters + string.digits
    verification_code = ''.join(random.choice(all_characters) for _ in range(8))
    new_verification_code = models.VerifyCode(
        username=username,
        email=email,
        verification_code=verification_code,
        expiration_time=datetime.datetime.now() + datetime.timedelta(minutes=5)
    )
    db.session.add(new_verification_code)
    db.session.commit()
    try:
        with current_app.app_context():
            mail = Mail(current_app)
            msg = Message(subject='注册验证码',
                          sender= mail.default_sender,
                          recipients=[email],  # 收件人地址列表
                          body=f'【失物招领系统】您的注册验证码是：{verification_code}，5分钟有效')
            mail.send(msg)
            return {'msg':'验证码发送成功'},200
    except Exception as e:
        return  {'msg':'验证码发送失败'},400

@auth_bp.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)
    checkpassword = data.get('checkpassword', None)
    verifycode = data.get('verifycode', None)
    if not username or not email or not password or not checkpassword or not verifycode:
        return jsonify({"msg": "缺少参数"}), 400
    if password != checkpassword:
        return {'msg': '两次密码不相同'}, 400
    if len(password) < 6:
        return {'msg': '验证码过短'}, 400
    dbverifycode = models.VerifyCode.query.filter(models.VerifyCode.username ==username and models.VerifyCode.email == email).first()
    if not dbverifycode:
        return {'msg':'验证码不存在或已过期'},400
    if dbverifycode.expiration_time < datetime.datetime.now():
        return {'msg':'验证码已过期，请重新发送'},400
    if verifycode != dbverifycode.verification_code:
        return {'msg':'验证码错误'},400
    try:
        new_user = models.User(username=username, email=email, password=password, role='editor')
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'msg': '注册失败'}, 400
    return {'msg':'注册成功'},200



