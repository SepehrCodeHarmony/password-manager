import random
import string
import bcrypt

def gen_password(username):
    username = username
    characters = string.ascii_letters + string.digits + string.punctuation
    genpassword = ''.join(random.choices(characters, k=20)).encode()
    gensalt = bcrypt.gensalt()

    return genpassword, gensalt

