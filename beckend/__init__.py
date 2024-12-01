from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from db import db
from auth import auth_bp
from items import items_bp

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Jikedao_11@47.100.24.135/jikedaodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 替换为你的密钥
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600

app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)