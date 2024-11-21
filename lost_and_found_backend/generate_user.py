from app import app
from db import db
from models import User
from app import app

# 使用应用上下文（在应用没有运行的情况下进行数据库操作时需要）
with app.app_context():
    # 创建新用户实例
    new_user = User(
        username= 'admin',
        email= 'admin@example.com',
        password= '111111',
        role ='admin'
    )

    # 更标准的做法是使用 set_password 方法来设置密码
    # new_user.set_password('securepassword')

    # 将新用户添加到数据库会话中
    db.session.add(new_user)

    # 提交会话，将数据保存到数据库中
    db.session.commit()