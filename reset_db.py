from app import app, db, User, Video

with app.app_context():
    db.drop_all()
    db.create_all()


    # 初期動画データ
    videos = [
        Video(name="電話のかけ方", path="/static/videos/0_Replay_Final1701407673.MP4", category="telephone"),
        Video(name="連絡先の追加方法", path="/static/videos/1_Replay_Final1701408033.MP4", category="telephone"),
        Video(name="着信履歴の確認方法", path="/static/videos/2_Replay_Final1701408088.MP4", category="telephone"),
        Video(name="キーパッドの使い方", path="/static/videos/3_Replay_Final1701408462.MP4", category="telephone"),
    ]

    for video in videos:
        db.session.add(video)

    # コミット
    db.session.commit()

print('データベースがリセットされました。')
