import uuid
from pathlib import Path
from apps.app import db
from apps.analyze.models import UserText, GraphData
from apps.analyze.forms import UploadTextForm, DeleteForm, SetUp, SeveData
from flask import (
    Blueprint,
    render_template,
    current_app,
    send_from_directory,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
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

        magnification = [1 for _ in range(len(ids))]
        space = [1 for _ in range(len(ids) - 1)]
        height = 500
        width = 1000
        return redirect(
            url_for(
                "analyze.upload_file",
                ids=",".join(map(str, ids)),
                selected_type=selected_type,
                magnification=",".join(map(str, magnification)),
                space=",".join(map(str, space)),
                height=height,
                width=width,
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
    save_form = SeveData()
    # 例えば /uploads?ids=3,5,7&selected_type=h_nmr からそれぞれの値を取得
    ids = request.args.get("ids", "")
    selected_type = request.args.get("selected_type", "")
    magnification = request.args.get("magnification", "")
    space = request.args.get("space", "")
    height = int(request.args.get("height", 500))
    width = int(request.args.get("width", 1000))

    ids = list(map(int, ids.split(",")))
    magnification = list(map(float, magnification.split(",")))
    if space == "":
        space = []
    else:
        space = list(map(float, space.split(",")))

    ids_num = len(ids)
    user_texts = db.session.query(UserText).filter(UserText.id.in_(ids)).all()

    for i, _ in enumerate(ids):
        setup_form.magnification.append_entry(magnification[i])
        if i < len(space):
            setup_form.space.append_entry(space[i])

    setup_form.aspect_ratio.data = f"{height},{width}"

    print(setup_form.magnification.data)
    print(setup_form.space.data)
    print(type(setup_form.magnification.data))

    if selected_type in ["h_nmr", "c_nmr", "f_nmr"]:
        graph_html = nmr(
            user_texts=user_texts,
            selected_type=selected_type,
            magnification=magnification,
            space=space,
            height=height,
            width=width,
        )
        return render_template(
            "analyze/graph.html",
            setup_form=setup_form,
            save_form=save_form,
            graph_html=graph_html,
            ids=",".join(map(str, ids)),
            selected_type=selected_type,
            ids_num=ids_num,
        )


@al.route("/renew", methods=["POST"])
def renew():
    setup_form = SetUp(request.form)

    ids = request.form.get("ids", "")
    ids = list(map(int, ids.split(",")))
    selected_type = request.form.get("selected_type", "")
    magnification = setup_form.magnification.data
    space = setup_form.space.data
    aspect_ratio = list(map(int, setup_form.aspect_ratio.data.split(",")))
    height, width = aspect_ratio

    return redirect(
        url_for(
            "analyze.upload_file",
            ids=",".join(map(str, ids)),
            selected_type=selected_type,
            magnification=",".join(map(str, magnification)),
            space=",".join(map(str, space)),
            height=height,
            width=width,
        )
    )


@al.route("/save_data", methods=["POST"])
def save_data():
    save_form = SeveData(request.form)

    name = save_form.name.data.strip()
    if name == "":
        return jsonify({"valid": False, "message": "名前を入力してください"})

    exists = GraphData.query.filter_by(
        name=name
    ).first()  # その名前のデータが既に存在するかどうかを調べる
    if exists:
        return jsonify({"valid": False, "message": "同じ名前が既に存在します"})

    selected_type = request.form.get("selected_type", "")
    magnification = list(
        map(float, request.form.get("magnification", "").strip("[]").split(","))
    )
    if request.form.get("space", "") == "[]":
        space = []
    else:
        space = list(map(float, request.form.get("space", "").strip("[]").split(",")))
    aspect_ratio = list(map(int, request.form.get("aspect_ratio", "").split(",")))
    height, width = aspect_ratio
    name = save_form.name.data

    print(selected_type)
    print(magnification)
    print(space)
    print(aspect_ratio)
    print(name)

    settings = {
        "selected_type": selected_type,
        "aspect_ratio": aspect_ratio,
        "magnification": magnification,
        "space": space,
    }

    ids = request.form.get("ids", "")
    ids = list(map(int, ids.split(",")))
    user_text = UserText.query.filter(UserText.id.in_(ids)).all()

    graph_data = GraphData(name=name, settings=settings, files=user_text)
    db.session.add(graph_data)
    db.session.commit()

    return redirect(
        url_for(
            "analyze.upload_file",
            ids=",".join(map(str, ids)),
            selected_type=selected_type,
            magnification=",".join(map(str, magnification)),
            space=",".join(map(str, space)),
            height=height,
            width=width,
        )
    )
