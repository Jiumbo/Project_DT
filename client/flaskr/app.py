from flask import Flask, render_template, request
from flaskr.routes.index import index_bp
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app=app)

app.register_blueprint(index_bp)


@app.route("/socket")
def socket():
    return render_template("test_socket.html")


@socketio.on("connect")
def test_connect():
    pass



