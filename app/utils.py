from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# generate and return hash of an string
def get_hash_from_str(password: str):
    hashed = pwd_context.hash(password)
    return hashed


# verify password
def verifyPassword(given_pass: str, hashed_pass: str):
    return pwd_context.verify(given_pass, hashed_pass)
