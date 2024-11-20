from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from functools import wraps
import bcrypt  # 用于密码哈希
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 替换为你的密钥
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

# 假设的用户数据库（在实际应用中，你会从数据库中查询用户）
users_db = {
    'admin': {
        'password': bcrypt.hashpw(b'111111', bcrypt.gensalt()).decode('utf-8')  # 已哈希的密码
    }
}


# 登录路由
@app.route('/vue-admin-template/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing credentials"}), 400

    # 从数据库中获取用户（在实际应用中，你会查询数据库）
    user = users_db.get(username, None)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # 将主题信息（这里以用户名作为主题）包含在identity字典中
        identity_info = {'username': username}
        access_token = create_access_token(identity=username)
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({"msg": "用户名或密码错误"}), 401


# 受保护的路由示例
@app.route('/vue-admin-template/user/info', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(name='admin', avatar='avatar'), 200

@app.route('/vue-admin-template/user/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Successfully logged out"})
    unset_jwt_cookies(response)
    return response, 200
if __name__ == '__main__':
    app.run(debug=True)