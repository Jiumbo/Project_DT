import firebase_admin.auth
from flask import Blueprint
from flask import render_template, request, redirect, url_for, session
import json
import firebase_admin
from firebase_admin import auth

login_bp = Blueprint("login", __name__)


@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        id_token = request.get_json().get("idToken")
        try:
            decoded_token = auth.verify_id_token(id_token)
            uid = decoded_token["uid"]
            session["user"] = uid
            print(uid)
            return redirect(url_for("user.dashboard"))
        except firebase_admin.auth.InvalidIdTokenError:
            return "Login failed"
    return render_template("login.html")


@login_bp.route("/logout")
def logout():
    session.pop("user")
    return redirect(url_for("login.login"))
