import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import firestore

from google.cloud.firestore_v1.client import Client

from dotenv import dotenv_values


env_variables = dotenv_values()

cred_values = { \
	"type": env_variables["type"], \
	"project_id": env_variables["project_id"], \
	"private_key_id": env_variables["private_key_id"], \
	"private_key": env_variables["private_key"].replace('\\n', '\n'), \
	"client_email": env_variables["client_email"], \
	"client_id": env_variables["client_id"], \
	"auth_uri": env_variables["auth_uri"], \
	"token_uri": env_variables["token_uri"], \
	"auth_provider_x509_cert_url": env_variables["auth_provider_x509_cert_url"], \
	"client_x509_cert_url": env_variables["client_x509_cert_url"], \
	"universe_domain": env_variables["universe_domain"], \
}

cred = Certificate(cred_values)

app = firebase_admin.initialize_app(credential=cred)

db: Client = firestore.client()
