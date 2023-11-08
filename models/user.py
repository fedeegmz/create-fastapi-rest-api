# Python
from datetime import date, datetime
from typing import Optional, Union
from bson import ObjectId

# Pydantic
from pydantic import BaseModel, EmailStr, Field


class BaseUser(BaseModel):
    _id: Optional[ObjectId]
    id: str = Field(default_factory=lambda:str(ObjectId()))
    username: str = Field(
        ...,
        min_length = 4,
        max_length = 15
    )
    name: str = Field(
        ...,
        min_length = 3,
        max_length = 20
    )
    lastname: str = Field(
        ...,
        min_length = 3,
        max_length = 20
    )
    email: Union[EmailStr, str] = Field(...)
    birth_date: Optional[date] = Field(default=None)

class User(BaseUser):
    disabled: bool = Field(default=False)
    created: Union[datetime, str] = Field(default=str(datetime.now()))
    
class UserDb(User):
    password: str = Field(
        ...,
        min_length = 8,
        max_length = 64
    )

    class Config:
        json_schema_extra = {
            "example": {
                "username": "ironman",
                "name": "Anthony",
                "lastname": "Stark",
                "email": "tony@starkindustries.com",
                "birth_date": str(date(2000, 12, 25)),
                "password": "ILoveMark40"
            }
        }