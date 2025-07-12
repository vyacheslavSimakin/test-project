from typing import Annotated, Any
from fastapi import Depends
from app.models import TokenData
from app.db.postgress import database
from app.logic.auth import get_current_user_, oauth2_scheme

TokenDep = Annotated[TokenData, Depends(get_current_user_)]

async def db_conn():
    async with database.pool.acquire() as connection:
        yield connection

async def get_current_user(db_conn: Annotated[Any, Depends(db_conn)],
                           token: Annotated[str, Depends(oauth2_scheme)]):
    return await get_current_user_(token, db_conn)
