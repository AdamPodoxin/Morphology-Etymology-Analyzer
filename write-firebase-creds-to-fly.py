import subprocess

from firebase import get_firebase_credentials


firebase_credentials = get_firebase_credentials()

# subprocess.run(f"fly secrets set {' '.join(list(map(lambda key: f'{key}={firebase_credentials[key]}', firebase_credentials)))}")
print(f"fly secrets set {' '.join(list(map(lambda key: f'{key}={firebase_credentials[key]}', firebase_credentials)))}")

print("Set keys", firebase_credentials.keys(), "on Fly")