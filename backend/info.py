import json

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from models import InfoPost

info_bp = Blueprint('info', __name__)

# 获取当前用户发布的信息列表
@info_bp.route('/api/info/user', methods=['GET'])
@jwt_required()
def get_user_info_list():
    try:
        # 将 get_jwt_identity() 返回的 JSON 字符串解析为字典
        identity = json.loads(get_jwt_identity())
        current_user = identity['username']  # 获取用户名
    except  Exception as e:
        return jsonify({'msg': 'Invalid JWT token format'}), 400
    posts = InfoPost.query.filter_by(upload_user=current_user, is_active=True).order_by(InfoPost.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])

# 获取信息列表
@info_bp.route('/api/info/all', methods=['GET'])
@jwt_required()
def get_info_list():
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    query = InfoPost.query.filter_by(is_active=True)
    if search:
        query = query.filter(InfoPost.title.like(f'%{search}%'))
    if category:
        query = query.filter(InfoPost.category==category)
    posts = query.order_by(InfoPost.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])

# 发布信息
@info_bp.route('/api/info', methods=['POST'])
@jwt_required()
def create_info():
    try:
        # 将 get_jwt_identity() 返回的 JSON 字符串解析为字典
        identity = json.loads(get_jwt_identity())
        current_user = identity['username']  # 获取用户名
    except  Exception as e:
        return jsonify({'msg': 'Invalid JWT token format'}), 400
    data = request.json

    required_fields = ['title', 'content', 'category']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'字段 {field} 是必填项'}), 400

    new_post = InfoPost(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        upload_user=current_user
    )
    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201

# 编辑信息
@info_bp.route('/api/info/<int:id>', methods=['PUT'])
@jwt_required()
def update_info(id):
    try:
        # 将 get_jwt_identity() 返回的 JSON 字符串解析为字典
        identity = json.loads(get_jwt_identity())
        current_user = identity['username']  # 获取用户名
    except  Exception  as e:
        return jsonify({'msg': 'Invalid JWT token format'}),400
    data = request.json

    post = InfoPost.query.get_or_404(id)
    if post.upload_user != current_user:
        return jsonify({'error': '无权编辑此信息'}), 403

    post.title = data.get('title', post.title)
    post.content = data.get('content', post.content)
    post.category = data.get('category', post.category)
    db.session.commit()

    return jsonify(post.to_dict())

# 删除信息
@info_bp.route('/api/info/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_info(id):
    try:
        # 将 get_jwt_identity() 返回的 JSON 字符串解析为字典
        identity = json.loads(get_jwt_identity())
        current_user = identity['username']  # 获取用户名
    except  Exception  as e:
        return jsonify({'msg': 'Invalid JWT token format'}), 400
    post = InfoPost.query.get_or_404(id)
    if post.upload_user != current_user and identity['role'] != 'admin':
        return jsonify({'error': '无权删除此信息'}), 403
    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': '信息已删除'})