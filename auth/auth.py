# Python
from datetime import datetime, timedelta
from typing import Union

# FastAPI
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

# PassLib
from passlib.context import CryptContext

# JWT
from jose import jwt, JWTError

# security
from security.config import settings

# database
from database.mongo_client import mongodb_client

# models
from models.user import UserIn
from models.token import TokenData


JWT_SECRETKEY = settings.jwt_secretkey
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(
    schemes = ["bcrypt"],
    deprecated = "auto"
    )


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = mongodb_client.users_db.find_one({"username": username})
    
    if not user:
        return False
    
    user = UserIn(**user)
    
    if not verify_password(password, user.password):
        return False
    
    del user.password

    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, JWT_SECRETKEY, algorithm=ALGORITHM)


async def get_current_user(token = Depends(oauth2_scheme)):
    print("En get_current_user")
    credentials_exception = HTTPException(
        status_code = status.HTTP_400_BAD_REQUEST,
        headers = {"WWW-Authenticate": "Bearer"},
        detail = {
            "errmsg": "Could not validate credentials"
        }
    )
    
    try:
        payload = jwt.decode(token, JWT_SECRETKEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(username)
        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
    
    except JWTError:
        raise credentials_exception
    
    user = mongodb_client.users_db.find_one({"username": token_data.username})

    if not user:
        raise credentials_exception
    
    user = UserIn(**user)
    
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Inactive user"
            }
        )
    
    return user