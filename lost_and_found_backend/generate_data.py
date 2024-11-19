from app import app
from db import db
from models import LostItem
from datetime import datetime, timedelta
import random
from faker import Faker

# 初始化 Faker
faker = Faker()

def generate_sample_data(count=100):
    categories = ['雨伞', '眼镜', '3C电子', '文具', '其他']
    locations = ['教学楼A区', '图书馆', '实验室B区', '自习室C区', '食堂', '操场', '宿舍区']
    sample_data = []

    # 生成随机数据
    for _ in range(count):
        found_date = faker.date_between(start_date='-30d', end_date='today')  # 过去30天内随机日期
        sample_data.append({
            'upload_user': faker.first_name(),  # 随机上传用户
            'item_name': faker.word() + random.choice(['雨伞', '眼镜', '耳机', '笔记本', '水杯']),  # 随机物品名称
            'category': random.choice(categories),  # 随机类别
            'found_date': found_date,  # 随机拾得日期
            'location': random.choice(locations),  # 随机拾得地点
            'description': faker.sentence(nb_words=10),  # 随机描述
            'contact_info': faker.email(),  # 随机联系方式
            'claimed': random.choice([True, False]),  # 随机认领状态
            'claimed_user': faker.first_name() if random.choice([True, False]) else None  # 如果已认领则生成认领用户
        })

    # 插入数据到数据库
    with app.app_context():
        for data in sample_data:
            item = LostItem(**data)
            db.session.add(item)
        db.session.commit()
        print(f"{count} sample records inserted successfully")

if __name__ == '__main__':
    generate_sample_data(count=500)  # 生成 500 条数据

