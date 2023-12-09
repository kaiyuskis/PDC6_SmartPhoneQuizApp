from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re, os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)


# データベースのモデル
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

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
katakana_pattern = re.compile(r'^[\u30A1-\u30F6\s]')
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
        name = request.form['name']
        password = request.form['password']

        # ユーザー名の重複をチェック
        user = User.query.filter_by(name=name).first()
        if user:
            return render_template('register.html', error='この名前は既に登録されています。')

        # 新規ユーザーの作成とデータベースへの追加
        new_user = User(name=name)
        new_user.set_password(password)  # パスワードをハッシュ化して保存
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='正しい名前とパスワードを入力してください。')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('home.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/telephone')
def telephone():
    videos = Video.query.filter_by(category='telephone').all()  # 仮にカテゴリが 'telephone' でフィルタリング
    return render_template('telephone.html', videos=videos)

@app.route('/mail')
def mail():
    return render_template('mail.html')

@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/internet')
def internet():
    return render_template('internet.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/screen')
def screen():
    return render_template('screen.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/watch_video/<int:video_id>')
@login_required
def watch_video(video_id):
    # 視聴状態がすでに存在するかどうかを確認し、存在しない場合は作成
    watch_status = WatchStatus.query.filter_by(user_id=current_user.id, video_id=video_id).first()
    if not watch_status:
        watch_status = WatchStatus(user_id=current_user.id, video_id=video_id, watched=True)
        db.session.add(watch_status)
    else:
        watch_status.watched = True
    db.session.commit()

    return jsonify({'message': 'Watch status updated'})

if __name__ == "__main__":
    app.run(debug=True)
