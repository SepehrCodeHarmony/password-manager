from cryptography.fernet import Fernet
from user_auth.main import main
import bcrypt

original_key = Fernet.generate_key()
salt = bcrypt.gensalt()
peper = bcrypt.gensalt()

try:
    with open('bins/peper', 'rb') as file:
        peper = file.read()
except FileNotFoundError:
    with open('bins/peper', 'wb') as file:
        file.write(peper) 
             
try:
    with open('bins/key', 'rb') as file:
        password = file.read()
except FileNotFoundError:
    with open("bins/key", "wb") as file:
        file.write(original_key)

try:
    with open('bins/salt', 'rb') as file:
        salt = file.read()
except FileNotFoundError:
    with open("bins/salt", "wb") as file:  
        file.write(salt)

try:
    with open('user_auth/database/database.db') as file:
        pass
except FileNotFoundError:
    main('sign up')