from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re, os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


# データベースのテーブル作成
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sei = db.Column(db.String(50), nullable=False)
    mei = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day = db.Column(db.Integer, nullable=False)

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False) # 動画タイトル
    path = db.Column(db.String(100), nullable=False) # ファイルパス
    category = db.Column(db.String(100)) # 動画のカテゴリ

class WatchStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))
    watched = db.Column(db.Boolean, default=False)

# 変数の初期化
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# ルーティング
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        sei = request.form['sei']
        mei = request.form['mei']
        name = request.form['name']
        year = request.form['year']
        month = request.form['month']
        day = request.form['day']

        # ユーザー名の重複をチェック
        user = User.query.filter_by(name=name).first()
        if user:
            return render_template('register.html', error='この表示名は既に使われています。他の表示名を入力してください。')

        else:
            new_user = User(sei=sei, mei=mei, name=name, year=year, month=month, day=day)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']

        user = User.query.filter_by(name=name).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='入力した情報が間違っているか、登録されていません。')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/telephone')
@login_required
def telephone():
    videos = Video.query.filter_by(category='telephone').all()  # 仮にカテゴリが 'telephone' でフィルタリング
    status = WatchStatus.query.all()
    return render_template('telephone.html', videos=videos, status=status)

@app.route('/mail')
def mail():
    videos = Video.query.filter_by(category='mail').all()
    return render_template('mail.html', videos=videos)

@app.route('/camera')
def camera():
    videos = Video.query.filter_by(category='camera').all()
    return render_template('camera.html', videos=videos)

@app.route('/internet')
def internet():
    videos = Video.query.filter_by(category='internet').all()
    return render_template('internet.html', videos=videos)

@app.route('/map')
def map():
    videos = Video.query.filter_by(category='map').all()
    return render_template('map.html', videos=videos)

@app.route('/screen')
def screen():
    videos = Video.query.filter_by(category='screen').all()
    return render_template('screen.html', videos=videos)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/video/<int:id>')
def video(id):
    video = Video.query.filter_by(id=id)
    status = WatchStatus.query.filter_by(user_id=current_user.id, video_id=id).first()
    if not status:
        status = WatchStatus(user_id=current_user.id, video_id=id, watched=True)
        db.session.add(status)
    else:
        status.watched = True

    db.session.commit()

    return render_template('video.html', video=video)

if __name__ == "__main__":
    app.run(debug=True)
