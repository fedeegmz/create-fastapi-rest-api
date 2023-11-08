# FastAPI
from fastapi import APIRouter, Path, Body
from fastapi import HTTPException, status, Depends

# auth
from auth.auth import get_password_hash, get_current_user

# database
from database.mongo_client import mongodb_client

# models
from models.user import User, UserDB, UserIn

# util
from util.white_lists import get_usernames_in_db


router = APIRouter(
    prefix = "/users",
    responses = {status.HTTP_404_NOT_FOUND: {"error": "Not Found"}}
)


### PATH OPERATIONS ###

## register a user ##
@router.post(
    path = "/signup",
    status_code = status.HTTP_201_CREATED,
    response_model = User,
    summary = "Register a user",
    tags = ["Users"]
)
async def signup(
    user_data: UserIn = Body(...)
):
    user_dict: dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])
    if user_dict.get("birth_date", None):
        user_dict["birth_date"] = str(user_dict["birth_date"])
    
    if user_dict.get("username") in get_usernames_in_db():
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "Username exists"
            }
        )
    
    user = UserIn(**user_dict)
    
    returned_data = mongodb_client.users_db.insert_one(user.model_dump())
    if not returned_data.acknowledged:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = {
                "errmsg": "User not inserted"
            }
        )
    
    del user.password
    user._id = returned_data.inserted_id
    
    return user

## show users ##
@router.get(
    path = "/",
    status_code = status.HTTP_200_OK,
    response_model = list[User],
    summary = "Show all users",
    tags = ["Users"]
)
async def users():
    users_list = mongodb_client.users_db.find().limit(100)
    users_list = [User(**user) for user in users_list]
    
    return users_list

## show a user ##
@router.get(
    path = "/{username}",
    status_code = status.HTTP_200_OK,
    response_model = User,
    summary = "Show a user",
    tags = ["Users"]
)
async def user(username: str = Path(...)):
    user_db = mongodb_client.users_db.find_one({"username": username})
    
    if not user_db:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = {
                "errmsg": "User not found"
            }
        )
    
    user = User(**user_db)
    
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
    user = UserDB(**user)
    
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
    user = UserDB(**user)
    
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

@router.get(
    path = "/available-usernames",
    status_code = status.HTTP_200_OK,
    response_model = list,
    summary = "Get available usernames",
    tags = ["Users"]
)
async def get_available_usernames():
    return get_usernames_in_db()