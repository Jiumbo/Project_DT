from flask import Flask
from flaskr.routes.index import index_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
