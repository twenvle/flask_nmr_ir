from datetime import datetime
from apps.app import db


# db.Modelに継承することで，これはデータベースのテーブルと繋がるクラスであるとFlaskに伝えている
class UserText(db.Model):
    __tablename__ = "user_texts"
    id = db.Column(db.Integer, primary_key=True)
    # user_idはusersテーブルのidカラムを外部キーとして設定する
    # user_id = db.Column(db.String, db.ForeignKey("users.id")) テキストをアップロードしたユーザーのID
    text_path = db.Column(db.String)  # サーバー上に保存されているテキストのパス
    type = db.Column(db.String)  # テキストの種類（1H-NMR, 13C-NMR, 19F-NMR, FT-IRなど）
    # is_detected = db.Column(db.Boolean, default=False) 画像が検出済みかどうか
    created_at = db.Column(
        db.DateTime, default=datetime.now
    )  # テキストがアップロードされた日時
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # テキストが更新された日時
