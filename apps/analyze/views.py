from flask import Blueprint

dt  = Blueprint("detector", __name__, template_folder="templates")

@dt.route("/")
def index():
    