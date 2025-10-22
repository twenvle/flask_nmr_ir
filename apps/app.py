from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apps.config import config

db = SQLAlchemy()


def create_app(config_key):
    app = Flask(__name__)

    app.config.from_object(config[config_key])

    db.init_app(app)
    Migrate(app, db)

    from apps.analyze import views as analyze_views

    app.register_blueprint(analyze_views.al, url_prefix="/analyze")

    # from apps.data import views as data_views

    # app.register_blueprint(data_views.data, url_prefix="/data")

    return app


# app = create_app(config_key="development")
#
# if __name__ == "__main__":
# app.run(host="0.0.0.0", port=5000, debug=True)
