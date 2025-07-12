from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from app.models import TokenData, UserInDB
from os import getenv


SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = "HS256"

#to change id to uuid
#to add register

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):#move to helpers/utils
    return pwd_context.hash(password)


async def get_user_by_email(email: str, connection):
    user = await connection.fetchrow('''SELECT user_id, first_name, 
    last_name, password FROM users WHERE email = $1 ''', email)
    if user:
        return UserInDB(**user)

async def check_user_by_id(user_id: int, connection):
    user = await connection.fetchrow('''SELECT user_id, first_name
    FROM users WHERE user_id = $1 ''', int(user_id))
    if user:
        return True

async def authenticate_user(email: str, password: str, connection):
    user = await get_user_by_email(email, connection)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=1)
    print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user_(token: str, connection) -> TokenData:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        print(datetime.now(timezone.utc))
        user_id = payload.get('user_id')
        if user_id is None:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        token_data = TokenData(user_id=str(user_id),
                                name=payload.get('name'))
        print(token_data)
    except InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    user = await check_user_by_id(user_id=token_data.user_id, 
                                  connection=connection)
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return token_data