from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from colorama import Fore, Style
import bcrypt
import base64
import sys

"""
there is 2 salt here

the 1st one --> this taken as an argument. title 'gensalt'. and it's different for each password.
this will be saved in data base in a column named salt for each password

the 2nd  one --> this is wroten in this directory "bins/salt". title 'salt'

1st(gensalt) is used manually at the beginnig of the password
2nd salt is used for kdf using cryptography library
"""

def encrypt_pass(genpassword, gensalt):

    with open('bins/peper', 'rb') as file:
        peper = file.read()

    password_1 = gensalt + peper + genpassword
    
    with open('bins/key', 'rb') as file:
        password = file.read()

    with open('bins/salt', 'rb') as file:
        salt = file.read()

    key = bcrypt.kdf(
                            password= password,
                            salt= salt,
                            desired_key_bytes=32,
                            rounds= 50)

    final_key = base64.urlsafe_b64encode(key)

    f = Fernet(final_key)
    token = f.encrypt(password_1)

    return token

def decrypt_pass(token, gensalt):

    with open('bins/peper', 'rb') as file:
        peper = file.read()

    with open('bins/key', 'rb') as file:
        password = file.read()

    with open('bins/salt', 'rb') as file:
        salt = file.read()

    key  =bcrypt.kdf(
                            password= password,
                            salt= salt,
                            desired_key_bytes=32,
                            rounds= 50)

    final_key = base64.urlsafe_b64encode(key)

    f = Fernet(final_key)
    try:
        decrypted_password = f.decrypt(token).decode()
    except InvalidToken:
        BOLD = '\033[1m'
        END = '\033[0m'
        print(Fore.RED + f'{BOLD}InvalidToken: the token was encrypted with another key{END}' + Style.NORMAL)
        sys.exit()

    l = len(gensalt.decode()) + len(peper)
    decrypted_password = decrypted_password[l:]

    return decrypted_password