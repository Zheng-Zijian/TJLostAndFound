import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db
import models
from sqlalchemy import or_
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
import bcrypt  # 用于密码哈希
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Jikedao_11@47.100.24.135/jikedaodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 替换为你的密钥
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

# 登录路由
@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', None)
    password = data.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing credentials"}), 400

    # 从数据库中获取用户（在实际应用中，你会查询数据库）
    user = models.User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        # 将主题信息（这里以用户名作为主题）包含在identity字典中
        identity_info = {'username': username}
        access_token = create_access_token(identity= json.dumps({'username':username,'role':user.role}))
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({"msg": "用户名或密码错误"}), 401


# 受保护的路由示例
@app.route('/user/info', methods=['GET'])
@jwt_required()
def getUserInfo():
    try:
        identity = json.loads(get_jwt_identity())
        print(type(identity))
        return {'name':identity['username'], 'avatar':'avatar','roles':[identity['role']]}, 200
    except Exception as e:
        return jsonify({"msg":'无法获取用户信息'}), 401
@app.route('/user/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Successfully logged out"})
    unset_jwt_cookies(response)
    return response, 200
# 获取所有失物列表
@app.route('/api/items', methods=['GET'])
def get_items():
    category = request.args.get('category', '')  # 获取类别参数
    search = request.args.get('search', '')  # 获取搜索关键字
    claimed = request.args.get('claimed', '')  # 获取认领状态
    sort_order = request.args.get('sort', 'asc') # 获取排序方式，默认升序
    query = models.LostItem.query

    # 如果类别非空，则按类别筛选
    if category:
        query = query.filter(models.LostItem.category == category)

    # 如果搜索关键字非空，则模糊匹配物品名称或拾得地点
    if search:
        query = query.filter(or_(
            models.LostItem.item_name.like(f"%{search}%"),
            models.LostItem.location.like(f"%{search}%")
        ))
    if claimed == 'claimed':
        query = query.filter(models.LostItem.claimed == True)
    elif claimed == 'unclaimed':
        query = query.filter(models.LostItem.claimed == False)

    #    根据排序参数调整排序方式
    if sort_order == 'asc':
        query = query.order_by(models.LostItem.found_date.asc())
    elif sort_order == 'desc':
        query = query.order_by(models.LostItem.found_date.desc())
    else:
        raise ValueError(f"Invalid sort_order: {sort_order}")
    items = query.all()

    return jsonify([item.to_dict() for item in items])

# 添加失物记录
@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = models.LostItem(
        upload_user=data['upload_user'],
        item_name=data['item_name'],
        category=data['category'],
        location=data['location'],
        description=data['description'],
        contact_info=data['contact_info']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'status': 'success'})

# 认领失物

@app.route('/api/items/claim/<int:item_id>', methods=['POST'])
def claim_item(item_id):
    item = models.LostItem.query.get(item_id)
    if item:
        item.claimed = True
        item.claimed_user = request.json.get('claimed_user')
        db.session.commit()
        return jsonify({'status': 'claimed'})
    return jsonify({'status': 'not found'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)





