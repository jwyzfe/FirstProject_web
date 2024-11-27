from datetime import datetime, timedelta
import random
from pymongo import MongoClient
from faker import Faker

# MongoDB 연결
client = MongoClient("mongodb://localhost:27017/")
db = client["cocolabhub"]
collection = db["users"]

# Faker 생성
fake = Faker()

# Role 목록
role_choices = ['MEMBER', 'ADMIN', 'EDITOR']

# 데이터 생성
records = []
for _ in range(50):
    name = fake.name()
    email = fake.email() 
    roles = random.sample(role_choices, k=random.randint(1, len(role_choices)))
    create_date = fake.date_time_this_year()
    last_access_date = create_date + timedelta(days=random.randint(0, 30))

    record = {
        "name": name,
        "email": email,
        "roles": roles,
        "create_date": create_date,
        "last_access_date": last_access_date,
    }
    records.append(record)

# 데이터 삽입
collection.insert_many(records)

print("50개의 데이터가 삽입되었습니다.")
