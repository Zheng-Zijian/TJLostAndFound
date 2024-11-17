from flask import Flask, request, jsonify
from flask_cors import CORS
from db import db
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/lost_found_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db.init_app(app)

# 获取所有失物列表
@app.route('/api/items', methods=['GET'])
def get_items():
    category = request.args.get('category')
    search = request.args.get('search')

    query = models.LostItem.query
    if category:
        query = query.filter(models.LostItem.category == category)
    if search:
        query = query.filter(models.LostItem.item_name.like(f"%{search}%"))

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





