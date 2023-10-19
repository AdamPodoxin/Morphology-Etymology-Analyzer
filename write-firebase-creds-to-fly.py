import subprocess

from firebase import FirebaseCredentials


firebase_credentials = FirebaseCredentials.load_from_env()
env_dict = firebase_credentials.to_env_dict()

command = f"fly secrets set {' '.join(map(lambda key: f'{key}={env_dict[key]}', env_dict))}"
subprocess.run(command)

print("Set keys ", list(env_dict), "on Fly")
