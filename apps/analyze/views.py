import uuid
from pathlib import Path
from apps.app import db
from apps.analyze.models import UserText
from apps.analyze.forms import UploadTextForm, DeleteForm, SetUp
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
from apps.analyze.plot import nmr


al = Blueprint("analyze", __name__, template_folder="templates")


@al.route("/", methods=["GET", "POST"])
def index():
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
            user_text = UserText(
                text_path=text_uuid_file_name, type=selected_type
            )  # ファイル名ではなくデータベースの要素と考えた方が良い 一行分のレコード
            db.session.add(user_text)  # この段階ではまだIDは割り振られていない
            db.session.flush()  # IDを確定させる(commit or flush)
            ids.append(user_text.id)  # ファイル名よりもIDを使った方が良い

        db.session.commit()
        return redirect(
            url_for(
                "analyze.upload_file",
                ids=",".join(map(str, ids)),
                selected_type=selected_type,
            )
        )
        # リダイレクトで渡せるのは HTTPリクエスト（URL）経由だけなので、変数の中身はそのまま関数間で共有できないことに注意
        # 例: /uploads?ids=3,5,7&selected_type=h_nmr

    # delete_form = DeleteForm()

    return render_template("analyze/index.html", form=form)  # , delete_form=delete_form
    # getリクエスト: render_template()でフォームを表示
    # postリクエスト: 処理が終わったらredirect()で別のUPLへ
    #                このとき，render_template()だと二重送信の危険性がある


@al.route("/uploads")
def upload_file():
    setup_form = SetUp()
    # 例えば /uploads?ids=3,5,7&selected_type=h_nmr からそれぞれの値を取得
    ids = request.args.get("ids", "")
    selected_type = request.args.get("selected_type", "")

    ids = list(map(int, ids.split(",")))
    ids_num = len(ids)
    user_texts = db.session.query(UserText).filter(UserText.id.in_(ids)).all()

    for _ in ids:
        setup_form.magnification.append_entry()
        if _ == ids[-1]:
            continue
        setup_form.space.append_entry()

    if selected_type in ["h_nmr", "c_nmr", "f_nmr"]:
        magnification = [1 for _ in range(len(ids))]
        space = [1 for _ in range(len(ids))]
        graph_html = nmr(user_texts, selected_type, magnification, space)
        return render_template(
            "analyze/graph.html",
            setup_form=setup_form,
            graph_html=graph_html,
            ids=ids,
            selected_type=selected_type,
            ids_num=ids_num,
        )


@al.route("/renew", methods=["POST"])
def renew():
    setup_form = SetUp()
    magnification = setup_form.magnification.data
    space = setup_form.space.data
    aspect_ratio = list(map(int, setup_form.aspect_ratio.data.split(",")))
