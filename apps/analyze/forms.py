from flask_wtf.file import FileAllowed, MultipleFileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.fields import SelectField


class UploadTextForm(FlaskForm):
    # ファイルフィールドに必要なバリデーションを設定する
    texts = MultipleFileField(
        validators=[
            FileRequired("ファイルを指定してください。"),
            FileAllowed(["txt", "csv", "asc"], "サポートされていない形式です。"),
        ]
    )

    type = SelectField(
        "選択してください",
        types=[
            ("", "---"),
            ("h_nmr", "1H-NMR"),
            ("c_nmr", "13C-NMR"),
            ("f_nmr", "19F-NMR"),
            ("ir", "FT-IR"),
        ],
        default="",
    )

    submit = SubmitField("アップロード")


class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
