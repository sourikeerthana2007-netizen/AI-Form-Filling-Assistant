import os
import json

from cryptography.fernet import Fernet
from dotenv import load_dotenv


load_dotenv()

key = os.getenv("ENCRYPTION_KEY")

if not key:
    raise ValueError("ENCRYPTION_KEY is missing from .env")

fernet = Fernet(key.encode())


def save_profile(profile):

    data = json.dumps(profile).encode()

    encrypted_data = fernet.encrypt(data)

    with open("profile.enc", "wb") as file:
        file.write(encrypted_data)


def load_profile():

    if not os.path.exists("profile.enc"):
        return {}

    with open("profile.enc", "rb") as file:
        encrypted_data = file.read()

    decrypted_data = fernet.decrypt(encrypted_data)

    return json.loads(decrypted_data.decode())