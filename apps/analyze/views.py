import uuid
from pathlib import Path
from apps.app import db
from apps.analyze.models import UserText
from apps.analyze.forms import UploadTextForm, DeleteForm
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
    user_texts = db.session.query(UserText).all()

    # UploadTextFormを利用してバリデーションをする
    form = UploadTextForm()

    selected_type = form.type.data
    if form.validate_on_submit():
        # アップロードされたテキストファイルを取得する
        ids = []
        files = form.texts.data
        for file in files:
            # ファイルのファイル名と拡張子を取得し、ファイル名をuuidに変換する
            ext = Path(file.filename).suffix
            text_uuid_file_name = str(uuid.uuid4()) + ext

            # テキストを保存する
            text_path = Path(current_app.config["UPLOAD_FOLDER"], text_uuid_file_name)
            file.save(text_path) 

            # DBに保存する
            user_text = UserText(text_path=text_uuid_file_name, type=selected_type) # ファイル名ではなくデータベースの要素と考えた方が良い 一行分のレコード
            db.session.add(user_text) # この段階ではまだIDは割り振られていない
            db.session.flush() # IDを確定させる(commit or flush)
            ids.append(user_text.id) # ファイル名よりもIDを使った方が良い

        db.session.commit()
        return redirect(url_for("analyze.upload_file", ids=ids))

    # delete_form = DeleteForm()

    return render_template(
        "analyze/index.html", user_texts=user_texts, form=form
    )  # , delete_form=delete_form
    # getリクエスト: render_template()でフォームを表示
    # postリクエスト: 処理が終わったらredirect()で別のUPLへ
    #                このとき，render_template()だと二重送信の危険性がある


@al.route("/uploads")
def upload_file():

