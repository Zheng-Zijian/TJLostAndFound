from flask import Blueprint, request, jsonify
from db import db
import models
from sqlalchemy import or_
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
import json

items_bp = Blueprint('items', __name__)

@jwt_required()
@items_bp.route('/api/items', methods=['GET'])
def get_items():
    category = request.args.get('category', '')  # 获取类别参数
    search = request.args.get('search', '')  # 获取搜索关键字
    claimed = request.args.get('claimed', '')  # 获取认领状态
    sort_order = request.args.get('sort', 'asc') # 获取排序方式，默认升序
    upload_user = request.args.get('upload_user','') # 获取上传用户
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

    #  如果上传用户非空，则按上传用户筛选
    if upload_user:
        query = query.filter(models.LostItem.upload_user == upload_user)

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
@jwt_required()
@items_bp.route('/api/items', methods=['POST'])
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
@jwt_required()
@items_bp.route('/api/items/claim/<int:item_id>', methods=['POST'])
def claim_item(item_id):
    item = models.LostItem.query.get(item_id)
    if item:
        item.claimed = True
        item.claimed_user = request.json.get('claimed_user')
        db.session.commit()
        return jsonify({'status': 'claimed'})
    return jsonify({'status': 'not found'}), 404

#每个用户上传的失物
@jwt_required()
@items_bp.route('/api/items/<string:username>', methods=['GET'])
def get_user_items(username):
    # 获取排序参数（asc 或 desc），默认按降序排列（距离现在最近的在前）
    sort_order = request.args.get('sort', 'desc')

    # 查询数据库，获取该用户上传的所有失物记录
    query = models.LostItem.query.filter_by(upload_user=username)

    # 根据排序参数调整排序
    if sort_order == 'asc':
        query = query.order_by(models.LostItem.found_date.asc())
    elif sort_order == 'desc':
        query = query.order_by(models.LostItem.found_date.desc())
    else:
        return jsonify({'message': f'Invalid sort_order: {sort_order}'}), 400

    user_items = query.all()

    # 检查是否有数据
    if not user_items:
        return jsonify({'message': f'No items found for user {username}'}), 404

    # 转换为 JSON 格式并返回
    return jsonify([item.to_dict() for item in user_items])

#删除失物
@items_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(item_id):
    try:
        # 将 get_jwt_identity() 返回的 JSON 字符串解析为字典
        identity = json.loads(get_jwt_identity())
        user = identity['username']  # 获取用户名
    except (json.JSONDecodeError, KeyError) as e:
        return jsonify({'msg': 'Invalid JWT token format'}), 400

    # 查询数据库中的记录
    item = models.LostItem.query.get(item_id)

    # 如果记录不存在，返回 404
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    # 验证权限：确保当前用户是记录的上传者
    if item.upload_user != user:
        return jsonify({'message': 'Permission denied'}), 403

    # 删除记录
    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': f'Item {item_id} deleted successfully'})

# 每个用户上传的失物 - 新增
@items_bp.route('/api/items/<string:username>', methods=['POST'])
@jwt_required()
def add_user_item(username):
    data = request.json  # 获取前端发送的 JSON 数据
    # 从 JWT Token 获取当前用户信息
    identity = json.loads(get_jwt_identity())
    current_user = identity['username']  # 获取当前登录用户

    # 确保 Token 中的用户名与路径参数中的用户名一致
    if current_user != username:
        return jsonify({'message': 'User mismatch: Token does not match path username'}), 403
    # 确保请求中的用户名与路径中的用户名一致
    if data.get('upload_user') != username:
        return jsonify({'message': 'User mismatch'}), 403

    # 必需字段
    required_fields = ['upload_user', 'item_name', 'category', 'location', 'contact_info']

    # 检查缺少的字段
    missing_fields = [field for field in required_fields if not data.get(field)]
    if missing_fields:
        return jsonify(dict(message=f'Missing required fields: {", ".join(missing_fields)}')), 400

    # 创建新的失物记录
    new_item = models.LostItem(
        upload_user=data['upload_user'],
        item_name=data['item_name'],
        category=data['category'],
        location=data['location'],
        description=data.get('description'),  # 可选字段
        contact_info=data['contact_info']
    )
    db.session.add(new_item)  # 添加到数据库会话
    db.session.commit()  # 提交到数据库

    # 返回新增记录的详细信息
    return jsonify({
        'msg': 'Item added successfully',
        'item': new_item.to_dict()
    }), 201

#申请认领
@items_bp.route('/api/items/<int:item_id>/apply', methods=['POST'])
@jwt_required()
def apply_claim(item_id):
    # 获取当前用户信息
    identity = json.loads(get_jwt_identity())
    claimant_username = identity['username']  # 从JWT中获取用户名

    # 根据用户名查询数据库获取用户ID
    claimant_user = models.User.query.filter_by(username=claimant_username).first()
    if not claimant_user:
        return jsonify({'message': 'Claimant user not found'}), 404  # 如果用户不存在，返回404错误

    # 检查物品是否存在
    item = models.LostItem.query.get(item_id)
    if not item:
        return jsonify({'message': 'Item not found'}), 404

    # 检查物品是否已被认领
    if item.claimed:
        return jsonify({'message': 'Item already claimed'}), 400

    # 检查是否重复认领
    existing_request = models.ClaimRequest.query.filter_by(lost_item_id=item_id, claimant_user_id=claimant_user.id).first()
    if existing_request:
        return jsonify({'message': 'You have already applied for this item'}), 400

    # 获取上传者的用户ID
    uploader_user = models.User.query.filter_by(username=item.upload_user).first()
    if not uploader_user:
        return jsonify({'message': 'Uploader user not found'}), 404  # 如果上传者用户不存在，返回404错误

    # 创建认领申请
    claim_request = models.ClaimRequest(
        lost_item_id=item_id,
        claimant_user_id=claimant_user.id,
        uploader_user_id=uploader_user.id,  # 使用查询到的上传者用户ID
        status='pending'
    )
    db.session.add(claim_request)
    db.session.commit()

    return jsonify({'message': 'Claim request submitted successfully'}), 201


#处理认领申请
@items_bp.route('/api/items/<int:item_id>/claim/<int:claim_id>/action', methods=['POST'])
@jwt_required()
def handle_claim(item_id, claim_id):
    # 获取当前用户
    identity = json.loads(get_jwt_identity())
    current_user_id = identity['username']  # 从JWT中获取用户名

    # 根据用户名查询数据库获取用户ID
    current_user = models.User.query.filter_by(username=current_user_id).first()
    if not current_user:
        return jsonify({'message': 'Current user not found'}), 404

    # 获取认领请求
    claim_request = models.ClaimRequest.query.get(claim_id)
    if not claim_request:
        return jsonify({'message': 'Claim request not found'}), 404

    # 检查当前用户是否是上传者
    if claim_request.uploader_user_id != current_user.id:
        return jsonify({'message': 'Unauthorized to handle this claim'}), 403

    # 获取操作类型
    action = request.json.get('action')
    if action not in ['approve', 'reject']:
        return jsonify({'message': 'Invalid action'}), 400

    # 检查是否已经有认领请求被批准
    if action == 'approve':
        # 检查是否已经有认领请求被批准
        existing_approved_requests = models.ClaimRequest.query.filter(
            models.ClaimRequest.lost_item_id == item_id,
            models.ClaimRequest.status == 'approved'
        ).first()
        if existing_approved_requests:
            return jsonify({'message': 'Another claim has already been approved for this item'}), 400

        # 标记其他所有请求为rejected
        other_requests = models.ClaimRequest.query.filter(
            models.ClaimRequest.lost_item_id == item_id,
            models.ClaimRequest.id != claim_id
        ).all()
        for req in other_requests:
            req.status = 'rejected'
            db.session.add(req)

    # 处理认领请求
    claim_request.status = 'approved' if action == 'approve' else 'rejected'
    if action == 'approve':
        claim_request.lost_item.claimed = True
        claim_request.lost_item.claimed_user = claim_request.claimant.username  # 使用认领者的用户名
#   elif action == 'reject' and claim_request.lost_item.claimed:
#       claim_request.lost_item.claimed = False

    # 提交更改
    db.session.commit()

    return jsonify({'message': 'Claim request updated successfully', 'status': claim_request.status}), 200