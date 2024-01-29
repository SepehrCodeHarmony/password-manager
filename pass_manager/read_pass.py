from cryptography.fernet import Fernet
import bcrypt
import base64


def read_pass_from_database(token, gensalt):

    with open('bins/peper.bin', 'rb') as file:
        peper = file.read()

    with open('bins/key.bin', 'rb') as file:
        password = file.read()

    with open('bins/salt.bin', 'rb') as file:
        salt = file.read()

    key  =bcrypt.kdf(
                            password= password,
                            salt= salt,
                            desired_key_bytes=32,
                            rounds= 100)

    final_key = base64.urlsafe_b64encode(key)

    f = Fernet(final_key)
    decrypted_password = f.decrypt(token).decode()


    l = len(gensalt.decode()) + len(peper)
    decrypted_password = decrypted_password[l:]

    return decrypted_password