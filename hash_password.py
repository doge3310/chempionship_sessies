from bcrypt import checkpw, gensalt, hashpw


def hash(password: str):
    pwd_bytes = password.encode()
    hashed = hashpw(pwd_bytes, gensalt())
    return hashed.decode()


def verify(password: str, hashed: str):
    pwd_bytes = password.encode()
    hashed_bytes = hashed.encode()
    return checkpw(pwd_bytes, hashed_bytes)
