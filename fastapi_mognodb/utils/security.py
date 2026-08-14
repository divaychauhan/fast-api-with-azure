import os
import bcrypt
from datetime import datetime,timedelta,timezone
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM=os.getenv("JWT_ALGORITHM","HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES","60"))

def hash_password(password: str):
    hashed=bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt())
    return hashed.decode("utf-8")

def verify_password(plain_password:str,hashed_password:str):
    return bcrypt.checkpw(plain_password.encode("utf-8"),
                        hashed_password.encode("utf-8"))
    
def create_access_token(user_id:str):
    expire=datetime.now(timezone.utc)+timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={
        "sub":user_id,
        "exp":expire
    }
    
    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )