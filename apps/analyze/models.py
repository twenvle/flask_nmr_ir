from datetime import datetime
from apps.app import db


# db.Modelに継承することで，これはデータベースのテーブルと繋がるクラスであるとFlaskに伝えている
class UserImage(db.Model):
    __tablename__ = "user_images"
    id = db.Column(db.Integer, primary_key=True)
    # user_idはusersテーブルのidカラムを外部キーとして設定する
    # user_id = db.Column(db.String, db.ForeignKey("users.id")) 画像をアップロードしたユーザーのID
    image_path = db.Column(db.String)  # サーバー上に保存されている画像のパス
    # is_detected = db.Column(db.Boolean, default=False) 画像が検出済みかどうか
    created_at = db.Column(
        db.DateTime, default=datetime.now
    )  # 画像がアップロードされた日時
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # 画像が更新された日時
