from app import app
from db import db
from models import LostItem
from datetime import datetime

def generate_sample_data():
    # 示例数据
    sample_data = [
        {
            'upload_user': 'Alice',
            'item_name': '雨伞',
            'category': '雨伞',
            'found_date': datetime(2024, 11, 10),
            'location': '教学楼A区',
            'description': '红色雨伞，有黑色手柄',
            'contact_info': 'alice@example.com',
            'claimed': False,
            'claimed_user': None
        },
        {
            'upload_user': 'Bob',
            'item_name': '眼镜',
            'category': '眼镜',
            'found_date': datetime(2024, 11, 12),
            'location': '图书馆',
            'description': '黑框眼镜，左镜片有划痕',
            'contact_info': 'bob@example.com',
            'claimed': True,
            'claimed_user': 'John'
        },
        {
            'upload_user': 'Charlie',
            'item_name': '3C电子产品',
            'category': '3C电子',
            'found_date': datetime(2024, 11, 13),
            'location': '实验室B区',
            'description': '蓝色耳机，品牌 Sony',
            'contact_info': 'charlie@example.com',
            'claimed': False,
            'claimed_user': None
        },
        {
            'upload_user': 'David',
            'item_name': '笔记本',
            'category': '文具',
            'found_date': datetime(2024, 11, 15),
            'location': '自习室C区',
            'description': '黑色封皮，有计算机科学笔记',
            'contact_info': 'david@example.com',
            'claimed': False,
            'claimed_user': None
        },
        {
            'upload_user': 'Eve',
            'item_name': '水杯',
            'category': '其他',
            'found_date': datetime(2024, 11, 16),
            'location': '食堂',
            'description': '绿色塑料水杯，印有 "Hello World" 标志',
            'contact_info': 'eve@example.com',
            'claimed': True,
            'claimed_user': 'Alice'
        }
    ]

    # 插入数据
    with app.app_context():
        for data in sample_data:
            item = LostItem(**data)
            db.session.add(item)
        db.session.commit()
        print("Sample data inserted successfully")

if __name__ == '__main__':
    generate_sample_data()
