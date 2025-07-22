from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from uuid import UUID
from enum import Enum


class UserBaseModel(BaseModel):
    first_name: Annotated[str, Field(min_length=2, max_length=50, examples=["Bob"])]
    last_name: Annotated[str | None, Field(min_length=2, max_length=50, examples=["Beebop"], default=None)]


class UserCreateModel(UserBaseModel):
    email: Annotated[EmailStr, Field(min_length=5, max_length=255, examples=["bob@mail.com"])]
    role: str = 'Tester'
    password: str


class UserFullModel(UserBaseModel):
    user_id: int
    email: EmailStr


class UserModel(UserBaseModel):
    user_id: int#UUID


class UserUpdateModel(BaseModel):
    first_name: Annotated[str | None, Field(min_length=2, max_length=50, examples=["Bob"], default=None)]
    last_name: Annotated[str | None, Field(min_length=2, max_length=50, examples=["Beebop"], default=None)]

    role: str | None = None


#class Roles(Enum):#todo
#    MANAGER = 'Manager'
#    TESTER = 'Tester'


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int
    name: str 


class LoginData(BaseModel):#unused
    email: EmailStr
    password: str 


class UserInDB(UserModel):
    password: str


#test-case models
class Priority(Enum):
    CRITICAL = 'CRITICAL'
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'

    @classmethod
    def list_priorities(cls):
        return [i for i in cls] 
    

class StepBaseModel(BaseModel):
    description: str | None = None
    expected_result: str | None=None


class Step(StepBaseModel):
    step_id: UUID
        

class StepCreateModel(StepBaseModel):
    next_step_id: UUID | None=None 
    prev_step_id: UUID | None=None 


class StepUpdateModel(StepCreateModel):
    description: str | None=None


class TCCreateModel(BaseModel):
    name: str 
    description: str 
    pre_conditions: str | None = Field(None, alias='pre-conditions')
    project_id: UUID
    priority: Priority = Priority.MEDIUM


class TCUpdateModel(BaseModel):
    name: str | None = None
    description: str | None = None 
    pre_conditions: str | None = Field(None, alias='pre-conditions')
    priority: Priority | None = None


class TCListMember(BaseModel):
    test_case_id: UUID
    name: str
    priority: Priority