import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin import firestore

from google.cloud.firestore_v1.client import Client

from dotenv import load_dotenv
import os


class FirebaseCredentials:
	type: str
	project_id: str
	private_key_id: str
	private_key: str
	client_email: str
	client_id: str
	auth_uri: str
	token_uri: str
	auth_provider_x509_cert_url: str
	client_x509_cert_url: str
	universe_domain: str


	def __init__(
			self,
			type,
			project_id,
			private_key_id,
			private_key,
			client_email,
			client_id,
			auth_uri,
			token_uri,
			auth_provider_x509_cert_url,
			client_x509_cert_url,
			universe_domain
	):
		self.type = type
		self.project_id = project_id
		self.private_key_id = private_key_id
		self.private_key = private_key
		self.client_email = client_email
		self.client_id = client_id
		self.auth_uri = auth_uri
		self.token_uri = token_uri
		self.auth_provider_x509_cert_url = auth_provider_x509_cert_url
		self.client_x509_cert_url = client_x509_cert_url
		self.universe_domain = universe_domain
	
	
	def to_dict(self) -> dict[str, str]:
		return self.__dict__
	

	def to_env_dict(self):
		original_dict = self.to_dict()
		new_dict: dict[str, str] = {}

		for key in original_dict:
			new_key = f"firebase_{key}"
			new_dict[new_key] = original_dict[key]
		
		return new_dict
	

	def to_certificate(self):
		credentials = self.to_dict()
		credentials["private_key"] = credentials["private_key"].replace("__NEWLINE__", "\n").replace("__SPACE__", " ")

		return Certificate(credentials)


	@staticmethod
	def load_from_env():
		load_dotenv()

		return FirebaseCredentials( 
			type = os.getenv("firebase_type"), 
			project_id = os.getenv("firebase_project_id"), 
			private_key_id = os.getenv("firebase_private_key_id"), 
			private_key = os.getenv("firebase_private_key"), 
			client_email = os.getenv("firebase_client_email"), 
			client_id = os.getenv("firebase_client_id"), 
			auth_uri = os.getenv("firebase_auth_uri"), 
			token_uri = os.getenv("firebase_token_uri"), 
			auth_provider_x509_cert_url = os.getenv("firebase_auth_provider_x509_cert_url"), 
			client_x509_cert_url = os.getenv("firebase_client_x509_cert_url"), 
			universe_domain = os.getenv("firebase_universe_domain") 
		)
	

def initialize_firebase():
	credentials = FirebaseCredentials.load_from_env()

	certificate = credentials.to_certificate()
	app = firebase_admin.initialize_app(credential=certificate)
	db: Client = firestore.client()

	return (db)
