import os
from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from jose import jwt,JWTError
from models.user import User

security=HTTPBearer()

JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY","this-is-secert-key-flask")

JWT_ALGORITHM=os.getenv("JWT_ALGORITHM","HS256")

async def get_current_user(
    credentials:HTTPAuthorizationCredentials=Depends(security)
):
    token=credentials.credentials
    try:
        payload=jwt.decode(token,JWT_SECRET_KEY,algorithms=[JWT_ALGORITHM])
        user_id=payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token not authorized")
        
    except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid or expired token")
        
    user=User.objects(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")

    return user