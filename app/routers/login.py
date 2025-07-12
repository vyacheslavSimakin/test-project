from datetime import timedelta
from typing import Annotated, Any

from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Token, UserInDB
from app.dependencies import db_conn, get_current_user
from app.logic.auth import authenticate_user, create_access_token

login_router = APIRouter(tags=["login"])
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

@login_router.get("/me")
async def get_current(
    current_user: Annotated[UserInDB, Depends(get_current_user)]):
    return current_user 

@login_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_conn: Annotated[Any, Depends(db_conn)]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password,
                                   db_conn)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.user_id, "name": user.first_name},
          expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")