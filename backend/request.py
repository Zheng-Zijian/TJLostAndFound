import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ClaimRequest, LostItem, User, db  # 确保 db 已正确导入

claim_request_bp = Blueprint('claim_request', __name__)

@claim_request_bp.route('/api/claim-requests/sent', methods=['GET'])
@jwt_required()
def get_sent_requests():
    identity = json.loads(get_jwt_identity())
    current_user_id = identity['id']  # 获取当前登录用户
    sent_requests = ClaimRequest.query.filter_by(claimant_user_id=current_user_id).all()
    result = [req.to_dict() for req in sent_requests]
    return jsonify(result), 200


@claim_request_bp.route('/api/claim-requests/received', methods=['GET'])
@jwt_required()
def get_received_requests():
    identity = json.loads(get_jwt_identity())
    current_user_id = identity['id']  # 获取当前登录用户

    received_requests = ClaimRequest.query.filter_by(uploader_user_id=current_user_id).all()
    result = [req.to_dict() for req in received_requests]
    return jsonify(result), 200



@claim_request_bp.route('/api/claim-requests/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_sent_request(request_id):
    identity = json.loads(get_jwt_identity())
    current_user_id = identity['id']  # 获取当前登录用户
    claim_request = ClaimRequest.query.filter_by(id=request_id, claimant_user_id=current_user_id).first()
    
    if not claim_request:
        return jsonify({'error': 'Request not found or you are not authorized'}), 404
    
    db.session.delete(claim_request)
    db.session.commit()
    return jsonify({'message': 'Request deleted successfully'}), 200


@claim_request_bp.route('/api/claim-requests/<int:request_id>/update', methods=['PATCH'])
@jwt_required()
def update_request_status(request_id):
    data = request.get_json()
    status = data.get('status')
    if status not in ['pending', 'approved', 'rejected']:
        return jsonify({'msg': 'Invalid status value'}), 400

    identity = json.loads(get_jwt_identity())
    current_user_id = identity['id']  # 获取当前登录用户
    claim_request = ClaimRequest.query.filter_by(id=request_id, uploader_user_id=current_user_id).first()
    
    if not claim_request:
        return jsonify({'error': 'Request not found or you are not authorized'}), 404

    claim_request.status = status
    db.session.commit()
    lost_item_id=claim_request.lost_item_id
    lostitem=LostItem.query.get(lost_item_id)
    if status=='approved':
        lostitem.claimed=True
        lostitem.claimed_user=claim_request.claimant.username
        db.session.commit()
        ClaimRequest.query.filter(ClaimRequest.lost_item_id==lost_item_id, ClaimRequest.id!=request_id).update({'status':'rejected'})
        db.session.commit()

    return jsonify({'message': 'Request status updated successfully'}), 200
