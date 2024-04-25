from flask import Blueprint
from flask import render_template, request, redirect, url_for
from markupsafe import escape
from flaskr import DT

index_bp = Blueprint("index", __name__)


@index_bp.route("/")
def hello_world():
    return render_template("index.html.jinja")


@index_bp.route("/set-ip", methods=["POST", "GET"])
def set_ip():
    if request.method == "POST":
        data = request.get_json().get("ipAddress")
        DT.set_ip(data)
        DT.setup()
    return "<p>Data<p>"
