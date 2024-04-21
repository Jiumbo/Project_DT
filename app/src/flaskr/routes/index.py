from flask import Blueprint

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def hello_world():
    return "<p>Hello World!</p>"
