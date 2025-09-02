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
    is_saved = db.Column(db.Boolean, default=False)  # 解析結果が保存済みかどうか
    batch_id = db.Column(
        db.Integer, db.ForeignKey("graph_data.id", name="usertexts_id"), nullable=True
    )  # 親(GraphData)への紐づけ　一時アップ時は未確定なのでNULL許可
    created_at = db.Column(
        db.DateTime, default=datetime.now
    )  # テキストがアップロードされた日時
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # テキストが更新された日時


class GraphData(db.Model):
    __tablename__ = "graph_data"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)  # 保存時の名前
    settings = db.Column(db.JSON)  # 解析に使用した設定（JSON形式で保存）
    files = db.relationship(
        "UserText", backref="graph_data"
    )  # 関連するUserTextのリスト
    created_at = db.Column(db.DateTime, default=datetime.now)  # データが保存された日時
    updated_at = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now
    )  # データが更新された日時
