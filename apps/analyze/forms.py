from flask_wtf.file import FileAllowed, MultipleFileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField
from wtforms.fields import FieldList, SelectField, FloatField, IntegerField, StringField


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
        choices=[
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
    submit = SubmitField("データを削除")


class SetUp(FlaskForm):
    magnification = FieldList(
        FloatField(
            "倍率",
            default=1,
        )
    )

    space = FieldList(
        FloatField(
            "プロットの間隔",
            default=1,
        )
    )

    aspect_ratio = SelectField(
        "縦横比",
        choices=[
            ("500,1000", " 1:2 "),
            ("563,937", " 3:5 "),
            ("643,857", " 3:4 "),
            ("750,750", " 1:1 "),
        ],
        default="500,1000",
    )

    oder = IntegerField(
        "順番",
        default=1,
    )

    submit = SubmitField("グラフを更新")


class SeveData(FlaskForm):
    name = StringField(
        "データ名",
    )

    submit = SubmitField("保存する")
