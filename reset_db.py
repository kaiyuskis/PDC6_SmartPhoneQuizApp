from app import app, db, User, Video


with app.app_context():
    db.drop_all()
    db.create_all()


    # 初期データ

    videos = [
        Video(name="電話のかけ方", path="../static/videos/電話のかけ方.mov", category="telephone"),
        Video(name="連絡先の追加方法", path="../static/videos/連絡先の追加方法.mov", category="telephone"),
        Video(name="着信履歴の確認方法", path="../static/videos/着信履歴の確認方法.mov", category="telephone"),
        Video(name="キーパッドの使い方", path="../static/videos/3_Replay_Final1701408462.MP4", category="telephone"),
        Video(name="受信メールの見方", path="../static/videos/3_Replay_Final1701408462.MP4", category="mail"),
        Video(name="メールの送り方", path="../static/videos/3_Replay_Final1701408462.MP4", category="mail"),
        Video(name="メールの保存方法", path="../static/videos/3_Replay_Final1701408462.MP4", category="mail"),
        Video(name="メールアドレスの確認方法", path="../static/videos/3_Replay_Final1701408462.MP4", category="mail"),
        Video(name="写真の撮り方", path="../static/videos/3_Replay_Final1701408462.MP4", category="camera"),
        Video(name="動画の撮り方", path="../static/videos/3_Replay_Final1701408462.MP4", category="camera"),
        Video(name="ズーム機能などの使い方", path="../static/videos/3_Replay_Final1701408462.MP4", category="camera"),
        Video(name="写真の見方", path="../static/videos/3_Replay_Final1701408462.MP4", category="camera"),
        Video(name="アルバムの作り方", path="../static/videos/3_Replay_Final1701408462.MP4", category="camera"),
        Video(name="検索方法", path="../static/videos/3_Replay_Final1701408462.MP4", category="internet"),
        Video(name="検索履歴の見方", path="../static/videos/3_Replay_Final1701408462.MP4", category="internet"),
        Video(name="アカウント管理について", path="../static/videos/3_Replay_Final1701408462.MP4", category="internet"),
        Video(name="ブックマークの仕方", path="../static/videos/3_Replay_Final1701408462.MP4", category="internet"),
        Video(name="マップの見方", path="../static/videos/3_Replay_Final1701408462.MP4", category="map"),
        Video(name="検索の方法", path="../static/videos/3_Replay_Final1701408462.MP4", category="map"),
        Video(name="保存の仕方", path="../static/videos/3_Replay_Final1701408462.MP4", category="map"),
        Video(name="ナビゲーションをする方法", path="../static/videos/3_Replay_Final1701408462.MP4", category="map"),
        Video(name="基本操作", path="../static/videos/3_Replay_Final1701408462.MP4", category="screen"),
        Video(name="応用編", path="../static/videos/3_Replay_Final1701408462.MP4", category="screen"),
        Video(name="おまけ", path="../static/videos/3_Replay_Final1701408462.MP4", category="screen"),
    ]



    for video in videos:
        db.session.add(video)

    # コミット
    db.session.commit()

print('データベースがリセットされました。')
