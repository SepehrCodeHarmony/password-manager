from cryptography.fernet import Fernet
import bcrypt

original_key = Fernet.generate_key()
salt = bcrypt.gensalt()

try:
    with open('bins/peper.bin', 'rb') as file:
        peper = file.read()
except FileNotFoundError:
    with open('bins/peper.bin', 'wb') as f:
        binary_data = bytes('plah plah plah', 'utf-8')
        f.write(binary_data)     
             
try:
    with open('bins/key.bin', 'rb') as file:
        password = file.read()
except FileNotFoundError:
    with open("bins/key.bin", "wb") as file:
        file.write(original_key)

try:
    with open('bins/salt.bin', 'rb') as file:
        salt = file.read()
except FileNotFoundError:
    with open("bins/salt.bin", "wb") as file:  
        file.write(salt)