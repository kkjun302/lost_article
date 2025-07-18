from extensions import db
from datetime import datetime

class LostItem(db.Model):
    id = db.Column(db.Integer, primary_key=True) #고유 번호
    title = db.Column(db.String(200), nullable=False)  # 제목
    student_id = db.Column(db.String(20), nullable=False)  # 학번
    location = db.Column(db.String(200), nullable=False)  # 발견 위치
    image = db.Column(db.String(300),nullable=True)  # 이미지 경로
    create_date = db.Column(db.DateTime, default = datetime.now)  # 생성 날짜 자동 추가
