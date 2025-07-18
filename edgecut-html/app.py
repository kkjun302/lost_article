import os  # os 모듈을 반드시 추가해야 합니다.
from flask import Flask
from extensions import db
from routes import init_routes

app = Flask(__name__)

# 1. 프로젝트의 현재 파일(app.py)이 위치한 디렉터리의 절대 경로를 가져옵니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. 절대 경로를 기준으로 'static/uploads' 폴더의 전체 경로를 만듭니다.
#    os.path.join을 사용하면 Windows(\)나 Mac/Linux(/)에 상관없이 올바른 경로가 만들어집니다.
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

# 3. Flask 앱 설정에 절대 경로로 지정합니다.
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 4. 앱이 시작될 때 UPLOAD_FOLDER 경로에 폴더가 없으면 자동으로 생성합니다.
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pybo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# 라우트 초기화
init_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
