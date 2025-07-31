from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


class UploadImageForm(FlaskForm):
    # ファイルフィールドに必要なバリデーションを設定する
    text = FileField(
        validators=[
            FileRequired("ファイルを指定してください。"),
            FileAllowed(["txt", "csv"], "サポートされていない形式です。"),
        ]
    )
    submit = SubmitField("アップロード")


class DeleteForm(FlaskForm):
    submit = SubmitField("削除")
