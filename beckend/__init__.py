from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from db import db
from auth import auth_bp
from items import items_bp
from info import info_bp


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Jikedao_11@47.100.24.135/jikedaodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 替换为你的密钥
jwt = JWTManager(app)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
app.config['MAIL_SERVER'] = 'smtp.yeah.net'  # yeah.net邮箱的SMTP服务器
app.config['MAIL_PORT'] = 465  # SMTP服务器端口（SSL通常使用465）
app.config['MAIL_USE_SSL'] = True  # 使用SSL加密
app.config['MAIL_USERNAME'] = 'jikedao@yeah.net'  # 你的yeah.net邮箱地址
app.config['MAIL_PASSWORD'] = 'NQhK7UJf4qLzqmGi'  # 你的yeah.net邮箱密码或应用专用密码
app.config['MAIL_DEFAULT_SENDER'] = 'jikedao@yeah.net'  # 默认发件人地址

app.register_blueprint(auth_bp)
app.register_blueprint(items_bp)
app.register_blueprint(info_bp)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)