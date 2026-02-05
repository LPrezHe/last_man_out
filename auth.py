import bcrypt

def hash_password(password: str) -> str:
    pw = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pw, salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed: str) -> bool:
    pw = password.encode("utf-8")
    hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(pw, hashed)

