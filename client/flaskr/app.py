from flask import Flask, render_template, request, redirect, url_for
from routes.login import login_bp
from routes.user import user_bp
from routes.graphs import graph_bp

app = Flask(__name__)
app.secret_key = "chiave"
app.register_blueprint(login_bp)
app.register_blueprint(user_bp)
app.register_blueprint(graph_bp)


@app.route("/")
def index():
    return redirect(url_for("login.login"))


if __name__ == "__main__":
    app.run(debug=True, port=8080)
