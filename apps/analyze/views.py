import uuid
from pathlib import Path
from apps.app import db
from apps.analyze.models import UserImage
from apps.analyze.forms import UploadImageForm, DeleteForm
from flask import (
    Blueprint,
    render_template,
    current_app,
    send_from_directory,
    redirect,
    url_for,
    flash,
    request,
)

al = Blueprint("analyze", __name__, template_folder="templates")


@al.route("/", methods=["GET", "POST"])
def index():
    user_images = db.session.query(UserImage).all()

    # UploadImageFormを利用してバリデーションをする
    form = UploadImageForm()
    if form.validate_on_submit():
        # アップロードされた画像ファイルを取得する
        files = form.texts.data
        for file in files:
            # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
            ext = Path(file.filename).suffix
            image_uuid_file_name = str(uuid.uuid4()) + ext

            # 画像を保存する
            image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
            file.save(image_path)

            # DBに保存する
            user_image = UserImage(image_path=image_uuid_file_name)
            db.session.add(user_image)

        db.session.commit()
        return redirect(url_for("analyze.index"))

    # delete_form = DeleteForm()

    return render_template(
        "analyze/index.html", user_images=user_images, form=form
    )  # , delete_form=delete_form
