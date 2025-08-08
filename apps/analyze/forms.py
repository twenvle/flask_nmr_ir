from flask_wtf.file import FileAllowed, MultipleFileField, FileRequired
from flask_wtf.form import FlaskForm, SelectField
from wtforms.fields.simple import SubmitField


class UploadImageForm(FlaskForm):
    # ファイルフィールドに必要なバリデーションを設定する
    texts = MultipleFileField(
        validators=[
            FileRequired("ファイルを指定してください。"),
            FileAllowed(["txt", "csv", "asc"], "サポートされていない形式です。"),
        ]
    )
    submit = SubmitField("アップロード")


class Setup(FlaskForm):
    choice = SelectField(
        "選択してください",
        choices=[
            ("h_nmr", "1H-NMR"),
            ("c_nmr", "13C-NMR"),
            ("f_nmr", "19F-NMR"),
            ("ir", "FT-IR"),
        ],
    )


class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
