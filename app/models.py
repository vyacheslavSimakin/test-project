from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
#from enum import Enum


class UserBaseModel(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=50, examples=["Bob"])]
    last_name: Annotated[str | None, Field(min_length=2, max_length=50, examples=["Beebop"], default=None)]


class UserCreateModel(UserBaseModel):
    email: Annotated[EmailStr, Field(min_length=5, max_length=255, examples=["bob@mail.com"])]
    role: str = 'Tester'
    password: str


class UserModel(UserBaseModel):
    user_id: int#UUID


class UserUpdateModel(BaseModel):
    first_name: Annotated[str | None, Field(min_length=2, max_length=50, examples=["Bob"], default=None)]
    last_name: Annotated[str | None, Field(min_length=2, max_length=50, examples=["Beebop"], default=None)]
    email: Annotated[EmailStr | None, Field(min_length=5, max_length=255, examples=["bob@mail.com"], default=None)]
    role: str | None = None


#class Roles(Enum):#todo
#    MANAGER = 'Manager'
#    TESTER = 'Tester'


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str
    name: str 


class LoginData(BaseModel):#unused
    email: EmailStr
    password: str 


class UserInDB(UserModel):
    password: str