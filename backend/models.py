from db import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
class LostItem(db.Model):
    __tablename__ = 'lost_items'
    id = db.Column(db.Integer, primary_key=True)
    upload_user = db.Column(db.String(50), nullable=False)
    item_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    found_date = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    contact_info = db.Column(db.String(100), nullable=False)
    claimed = db.Column(db.Boolean, default=False)
    claimed_user = db.Column(db.String(50), nullable=True)
    image_path = db.Column(db.String(100), nullable=True)
    def to_dict(self):
        return {
            'id': self.id,
            'upload_user': self.upload_user,
            'item_name': self.item_name,
            'category': self.category,
            'found_date': self.found_date.strftime('%Y-%m-%d'),
            'location': self.location,
            'description': self.description,
            'contact_info': self.contact_info,
            'claimed': self.claimed,
            'claimed_user': self.claimed_user
        }

#用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default='editor', nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, username, email, role, password):
        self.username = username
        self.email = email
        self.role = role
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class InfoPost(db.Model):
    __tablename__ = 'info_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    upload_user = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category': self.category,
            'upload_user': self.upload_user,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }

class VerifyCode(db.Model):
    __tablename__ = 'verification_codes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    verification_code = db.Column(db.String(255), nullable=False)
    expiration_time = db.Column(db.TIMESTAMP, nullable=False)

class ClaimRequest(db.Model):
    __tablename__ = 'claim_requests'

    id = db.Column(db.Integer, primary_key=True)
    lost_item_id = db.Column(db.Integer, db.ForeignKey('lost_items.id'), nullable=False)
    claimant_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    uploader_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 添加上传者字段
    status = db.Column(db.String(20), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    lost_item = db.relationship('LostItem', backref=db.backref('claim_requests', lazy=True))
    claimant = db.relationship('User', foreign_keys=[claimant_user_id], backref=db.backref('claim_requests', lazy=True))
    uploader = db.relationship('User', foreign_keys=[uploader_user_id], backref=db.backref('uploaded_claim_requests', lazy=True))  # 用于上传者关系

    def to_dict(self):
        return {
            'id': self.id,
            'lost_item_id': self.lost_item_id,
            'claimant_user_id': self.claimant_user_id,
            'uploader_user_id': self.uploader_user_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'uploader_username': self.uploader.username,
            'uploader_email': self.uploader.email,
            'claimant_username': self.claimant.username,
            'claimant_email': self.claimant.email,
            'item_name': self.lost_item.item_name,
            'category': self.lost_item.category,
            'found_date': self.lost_item.found_date.strftime('%Y-%m-%d'),
            'location': self.lost_item.location,
            'description': self.lost_item.description
        }