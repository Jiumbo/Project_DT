import firebase_admin
from firebase_admin import credentials, auth, firestore
import json

with open("client/flaskr/serviceAccountKey.json") as f:
    firebase_conf = json.loads(f.read())

cred = credentials.Certificate("client/flaskr/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
