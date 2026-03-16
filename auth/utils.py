from passlib.context import CryptContext
from datetime import datetime , timedelta ,timezone
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRY_MIN"))
RESET_TOKEN_EXPIRY_MIN = int(os.getenv("RESET_TOKEN_EXPIRY_MIN", "15"))

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    # BUG FIX: datetime.utcnow() deprecated — timezone-aware use pannrom
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRY_MIN)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_reset_token(data: dict) -> str:
    return create_access_token(data, expires_delta=timedelta(minutes=RESET_TOKEN_EXPIRY_MIN))
