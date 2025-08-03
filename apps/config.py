from pathlib import Path

basedir = Path(__file__).parent.parent


class BaseConfig:
    SECRET_KEY = "qwrty"  # Flask全体のセキュリティキー
    WTF_CSRF_SECRET_KEY = "aiueo"  # CSRF対策のためのセキュリティキー
    UPLOAD_FOLDER = str(
        Path(basedir, "apps", "past_data")
    )  # 画像アップロード先のフォルダ


class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # SQLAlchemyのオブジェクトの変更履歴の追跡機能をオン/オフする設定 普通はオフ
    SQLALCHEMY_ECHO = True


config = {
    "local": LocalConfig,
}
