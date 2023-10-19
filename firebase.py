import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import firestore

from google.cloud.firestore_v1.client import Client

from dotenv import load_dotenv
import os


def get_firebase_credentials():
	load_dotenv()

	try:
		return { \
			"type": os.getenv("type"), \
			"project_id": os.getenv("project_id"), \
			"private_key_id": os.getenv("private_key_id"), \
			"private_key": os.getenv("private_key").replace('\\n', '\n'), \
			"client_email": os.getenv("client_email"), \
			"client_id": os.getenv("client_id"), \
			"auth_uri": os.getenv("auth_uri"), \
			"token_uri": os.getenv("token_uri"), \
			"auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"), \
			"client_x509_cert_url": os.getenv("client_x509_cert_url"), \
			"universe_domain": os.getenv("universe_domain"), \
		}
	except:
		return {}


def initialize_firebase():
	cred = Certificate(get_firebase_credentials())
	app = firebase_admin.initialize_app(credential=cred)
	db: Client = firestore.client()

	return (db)
