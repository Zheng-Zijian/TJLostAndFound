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
    __tablename__ = 'user'
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
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class VerifyCode(db.Model):
    __tablename__ = 'verification_codes'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    verification_code = db.Column(db.String(255), nullable=False)
    expiration_time = db.Column(db.TIMESTAMP, nullable=False)