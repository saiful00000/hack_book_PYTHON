from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# generate and return hash of an string
def get_hash_from_str(password: str):
    hashed = pwd_context.hash(password)
    return hashed
