import os
from sqlalchemy import or_
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from extensions import db
from model import LostItem

# 허용할 이미지 파일 확장자 정의
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def init_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/introduction')
    def introduction():
        return render_template('introduction.html')

    @app.route('/create', methods=['POST'])
    def create_item():
        # 이 함수는 오직 form 데이터 처리 및 DB 저장만 담당합니다.
        title = request.form['title']
        student_id = request.form['student_id']
        location = request.form['location']
        
        if 'image' not in request.files or request.files['image'].filename == '':
            # 이미지 파일이 없는 경우의 처리 (예: 에러 메시지 또는 기본 이미지)
            # 여기서는 우선 리다이렉트 처리
            return redirect(request.referrer or url_for('write'))

        image = request.files['image']

        if image and allowed_file(image.filename):
            new_item = LostItem(title=title, student_id=student_id, location=location)
            db.session.add(new_item)
            db.session.commit()

            filename = secure_filename(f"lost_item_{new_item.id}{os.path.splitext(image.filename)[1]}")
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)

            new_item.image = filename
            db.session.commit()

            # 글 작성이 성공하면, 전체 목록 페이지로 이동시킵니다.
            return redirect(url_for('lost_item'))
        
        # 파일 형식이 올바르지 않은 경우
        return redirect(url_for('write'))


    @app.route('/lost-item', methods=['GET']) # 이제 POST는 필요 없으므로 'GET'만 처리합니다.
    def lost_item():
        # if request.method == 'POST': 블록 전체를 삭제합니다.
        
        search_query = request.args.get('q')
        
        if search_query:
            search_pattern = f"%{search_query}%"
            items = LostItem.query.filter(
                or_(
                    LostItem.title.ilike(search_pattern),
                    LostItem.location.ilike(search_pattern)
                )
            ).order_by(LostItem.create_date.desc()).all()
        else:
            items = LostItem.query.order_by(LostItem.create_date.desc()).all()
        
        # lost-item.html은 수정할 필요 없습니다.
        return render_template('lost-item.html', items=items, query=search_query)

    
    @app.route('/lost-item-admin')
    def lost_item_admin():
        # 관리자 페이지는 DB에서 모든 분실물 목록을 가져와서
        # lost_item_admin.html 템플릿으로 전달하는 역할만 합니다.
        items = LostItem.query.order_by(LostItem.create_date.desc()).all()
        return render_template('lost_item_admin.html', items=items)
    
    @app.route('/delete/<int:item_id>', methods=['POST'])
    def delete_item(item_id):
        item = LostItem.query.get_or_404(item_id)
        if item:
            # (선택사항) 서버에 저장된 이미지 파일도 함께 삭제하는 로직
            if item.image:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], item.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            
            db.session.delete(item)
            db.session.commit()
        return redirect(url_for('lost_item_admin'))
    
    # @app.route('/delete/<int:item_id>', methods = ['POST'])
    # def delete_item(item_id):
    #     item = LostItem.query.get(item_id)
    #     if item:
    #         db.session.delete(item)
    #         db.session.commit()
    #     return redirect(url_for('lost_item_admin'))


    @app.route('/write')
    def write():
        return render_template('write.html')
