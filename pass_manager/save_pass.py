from cryptography.fernet import Fernet
import bcrypt
import base64

def save_pass_in_database(genpassword, gensalt):

    with open('bins/peper.bin', 'rb') as file:
        peper = file.read()

    password_1 = gensalt + peper + genpassword
    
    with open('bins/key.bin', 'rb') as file:
        password = file.read()

    with open('bins/salt.bin', 'rb') as file:
        salt = file.read()

    key  = bcrypt.kdf(
                            password= password,
                            salt= salt,
                            desired_key_bytes=32,
                            rounds= 100)

    final_key = base64.urlsafe_b64encode(key)

    f = Fernet(final_key)
    token = f.encrypt(password_1)

    return token

