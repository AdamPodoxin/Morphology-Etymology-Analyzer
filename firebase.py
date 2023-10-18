import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from google.cloud.firestore_v1.client import Client

cred = credentials.Certificate('firebase-credentials.json')

app = firebase_admin.initialize_app(cred)

db: Client = firestore.client()
