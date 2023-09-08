from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint


"""
1] This below class method will autometically convert the data type as mentioned
2] It will give the error In standard way If we miss something in body
3] We can set default value so In case if frontend team doesn't provide the value then our
   class will give the default mentioned value. i.e. published
4] We can add optional key as well i.e. rating
4] We can pass this class name in def parameter
"""

class Post(BaseModel):
    title: str
    content :str
    published: bool = True

 
class UserOut(BaseModel):
    id : int
    email:EmailStr
    created_at: datetime

    class Config:
        orm_model = True

class GetPost(BaseModel):
    title: str
    content :str
    published: bool
    created_at: datetime
    id: int
    owner : UserOut
    
    class Config:
        orm_model = True


class UserCreate(BaseModel):
    email:EmailStr
    password:str


class UserLogin(BaseModel):
    email:EmailStr
    password: str

    class Config:
        orm_model = True

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)