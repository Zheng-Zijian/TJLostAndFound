from db import db
from datetime import datetime

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






