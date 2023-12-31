# FastAPI
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

# auth
from auth.auth import create_access_token, authenticate_user, get_current_user

# models
from models.user import User
from models.token import Token


ACCESS_TOKEN_EXPIRE_MINUTES = 20

router = APIRouter(
    prefix = "/login"
)


### PATH OPERATIONS ###

@router.post(
    path = "/token",
    response_model = Token,
    summary = "Login a user",
    tags = ["Token"]
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            headers = {"WWW-Authenticate": "Bearer"},
            detail = {
                "errmsg": "Incorrect username or password"
            }
        )
    
    access_token = create_access_token(
        data = {"sub": user.username},
        expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get(
    path = "/users/me",
    response_model = User,
    tags = ["Token"]
)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
