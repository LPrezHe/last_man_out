from passlib.hash import bcrypt

def hash_password(pw):
    return bcrypt.hash(pw)

def verify_password(pw, hashed):
    return bcrypt.verify(pw, hashed)
