from flask import Flask, request, jsonify
from models import db, LostItem

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/lost_found_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/items', methods=['GET'])
def get_items():
    items = LostItem.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = LostItem(
        item_name=data['item_name'],
        category=data['category'],
        location=data['location']
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
