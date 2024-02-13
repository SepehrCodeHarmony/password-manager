import bcrypt


def hash_with_salt(password:str):

    password = password.encode()
    salt = bcrypt.gensalt(rounds= 13)
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password


def check_password(password: str, hashed_password: str):

    return bcrypt.checkpw(password.encode(), hashed_password.encode())
