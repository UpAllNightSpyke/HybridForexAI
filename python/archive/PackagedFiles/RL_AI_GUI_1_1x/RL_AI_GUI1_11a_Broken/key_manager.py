import os
from cryptography.fernet import Fernet

# Define the key file path
key_file_path = 'encryption_key.key'

def get_cipher_suite():
    # Check if the key file exists
    if not os.path.exists(key_file_path):
        key = Fernet.generate_key()
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()

    return Fernet(key)

def get_key():
    if not os.path.exists(key_file_path):
        key = Fernet.generate_key()
        with open(key_file_path, 'wb') as key_file:
            key_file.write(key)
    else:
        with open(key_file_path, 'rb') as key_file:
            key = key_file.read()
    return key