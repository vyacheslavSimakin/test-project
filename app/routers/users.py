from fastapi import APIRouter, HTTPException, status, Path, Body, Depends
from typing import Annotated, Any
from app.models import UserModel, UserCreateModel, UserUpdateModel
from app.logic.users_logic import get_user_from_db, create_user_in_db,\
                                  update_user_in_db, delete_user_in_db,\
                                  get_users_from_db
from app.dependencies import db_conn, get_current_user

users_router = APIRouter(prefix='/users',
                         tags=['users'],
                         dependencies=[Depends(get_current_user)],
                         responses={404: {'description': 'Not found'}})


@users_router.get('/', response_model=list[UserModel])
async def get_users(db_conn: Annotated[Any, Depends(db_conn)]):
    users = await get_users_from_db(db_conn)
    return users


@users_router.get('/{id}', response_model=UserModel)
async def get_user(user_id: Annotated[int, Path(alias='id')],
                   db_conn: Annotated[Any, Depends(db_conn)]) -> Any:
    user = await get_user_from_db(user_id, db_conn)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user

    
@users_router.post('/') # SEND EMAIL AS A BACKGROUND TASK
async def create_user(body: Annotated[UserCreateModel, Body()],
                      db_conn: Annotated[Any, Depends(db_conn)]):
    try:
        await create_user_in_db(body, db_conn)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "User already exists")
    return "User created."


@users_router.patch('/{id}')
async def update_user(user_id: Annotated[int, Path(alias='id')], 
                body: Annotated[UserUpdateModel, Body()],
                db_conn: Annotated[Any, Depends(db_conn)]):
    try: 
        await update_user_in_db(user_id, body, db_conn)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    

@users_router.delete('/{id}')
async def delete_user(user_id: Annotated[int, Path(alias='id')],
                      db_conn: Annotated[Any, Depends(db_conn)]) -> str:
    try:
        await delete_user_in_db(user_id, db_conn)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    return 'User deleted.'