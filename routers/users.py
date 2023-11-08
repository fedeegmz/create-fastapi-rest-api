# Python
from typing import Union

# FastAPI
from fastapi import APIRouter, Path, Query, Body
from fastapi import HTTPException, status, Depends

# auth
from auth.auth import get_password_hash, get_current_user

# database
from database.mongo_client import mongodb_client

# models
from models.user import User, UserDb

# util
from util.white_lists import get_users_id_in_db, get_usernames_in_db


router = APIRouter(
    prefix = "/users"
)

### PATH OPERATIONS ###

## register a user ##
@router.post(
    path = "/register",
    status_code = status.HTTP_201_CREATED,
    response_model = User,
    summary = "Register a user",
    tags = ["Users"]
)
async def create_user(
    data: UserDb = Body(...)
):  
    if data.username in get_usernames_in_db():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Username exists"
            }
        )
    
    data.password = get_password_hash(data.password)
    returned_data = mongodb_client.users_db.insert_one(data.model_dump())
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "User not inserted"
            }
        )
    
    inserted_user = mongodb_client.users_db.find_one({"id": data.id})
    inserted_user = User(**inserted_user)

    return inserted_user


## get user by id ##
@router.get(
    path = "/{id}",
    status_code = status.HTTP_200_OK,
    response_model = User,
    tags = ["Users"],
    summary = "Get a user by ID"
)
async def get_user(
    id: str = Path(...)
):
    if not id in get_users_id_in_db():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect user ID"
            }
        )

    user = mongodb_client.users_db.find_one({"id": id})
    if not user:
        return None
    
    user = User(**user)

    return user


## get users or a user by username
@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    response_model = Union[User, list],
    tags = ["Users"],
    summary = "Get a user or users"
)
async def get_users(
    username: Union[str, None] = Query(default=None)
):
    if not username:
        users = mongodb_client.users_db.find().limit(25)
        users = [User(**user) for user in users]

        return users
    
    if not username.lower() in get_usernames_in_db():
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "errmsg": "Incorrect username"
            }
        )

    user = mongodb_client.users_db.find_one({"username": username})
    if not user:
        return None
    
    user = User(**user)

    return user


## update a user ##
@router.patch(
    path = "/{username}",
    status_code = status.HTTP_200_OK,
    response_model = User,
    summary = "Update a user",
    tags = ["Users"],
    deprecated = True
)
async def update_user(
    current_user: User = Depends(get_current_user),
    user_updates: list[dict] = Body(
        ...,
        example = [{"name": "Tony"}, {"lastname": "Stark"}]
    )
):
    user = mongodb_client.users_db.find_one({"username": current_user.username})
    user = User(**user)
    
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "User has already been deleted"
            }
        )
    
    # TODO
    # user_updated = mongodb_client.get_user_with_username_and_update(
    #     username = current_user.username,
    #     updates = user_updates
    # )
    
    # return user_updated


## delete a user ##
@router.delete(
    path = "/{username}",
    status_code = status.HTTP_200_OK,
    response_model = User,
    summary = "Delete a user",
    tags = ["Users"],
    deprecated = True
)
async def delete_user(
    current_user: User = Depends(get_current_user),
):
    user = mongodb_client.users_db.find_one({"username": current_user.username})
    user = User(**user)
    
    if user.disabled:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "User has already been deleted"
            }
        )
    
    # TODO
    # user_deleted = mongodb_client.get_user_with_username_and_update(
    #     username = current_user.username,
    #     updates = [{"disabled": True}]
    # )

    # return user_deleted
