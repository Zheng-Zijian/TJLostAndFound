from __init__ import app
from db import db
from models import InfoPost

with app.app_context():
    db.create_all()
    print("InfoPost 表已成功创建")

