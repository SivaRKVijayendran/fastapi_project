from passlib.context import CryptContext
from datetime import datetime , timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"] , deprecated = "auto")

def hash_password(password : str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password : str , hashed_password : str) -> bool:
    return pwd_context.verify(plain_password , hashed_password)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRY_MIN"))

def create_access_token(date : dict):
    to_encode = date.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MIN)

    to_encode.update({'exp' : expire})

    encode_jwt = jwt.encode(to_encode , SECRET_KEY , algorithm= ALGORITHM)

    return encode_jwt
