from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from db import db
from models import InfoPost

info_bp = Blueprint('info', __name__)

# 获取信息列表
@info_bp.route('/api/info', methods=['GET'])
def get_info_list():
    search = request.args.get('search', '')
    category = request.args.get('category', '')

    query = InfoPost.query.filter_by(is_active=True)
    if search:
        query = query.filter(InfoPost.title.contains(search))
    if category:
        query = query.filter_by(category=category)

    posts = query.order_by(InfoPost.created_at.desc()).all()
    return jsonify([post.to_dict() for post in posts])

# 获取单条信息详情
@info_bp.route('/api/info/<int:id>', methods=['GET'])
def get_info_detail(id):
    post = InfoPost.query.get_or_404(id)
    return jsonify(post.to_dict())

# 发布信息
@info_bp.route('/api/info', methods=['POST'])
@jwt_required()
def create_info():
    current_user = get_jwt_identity()
    data = request.json

    required_fields = ['title', 'content', 'category']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'字段 {field} 是必填项'}), 400

    new_post = InfoPost(
        title=data['title'],
        content=data['content'],
        category=data['category'],
        upload_user=current_user['username']
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': '信息发布成功', 'id': new_post.id}), 201

# 编辑信息
@info_bp.route('/api/info/<int:id>', methods=['PUT'])
@jwt_required()
def update_info(id):
    current_user = get_jwt_identity()
    post = InfoPost.query.get_or_404(id)

    if current_user['username'] != post.upload_user and current_user['role'] != 'admin':
        return jsonify({'error': '权限不足'}), 403

    data = request.json
    if 'title' in data:
        post.title = data['title']
    if 'content' in data:
        post.content = data['content']
    if 'category' in data:
        post.category = data['category']

    db.session.commit()
    return jsonify({'message': '信息修改成功'})

# 删除信息
@info_bp.route('/api/info/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_info(id):
    current_user = get_jwt_identity()
    post = InfoPost.query.get_or_404(id)

    if current_user['username'] != post.upload_user and current_user['role'] != 'admin':
        return jsonify({'error': '权限不足'}), 403

    post.is_active = False
    db.session.commit()
    return jsonify({'message': '信息删除成功'})
