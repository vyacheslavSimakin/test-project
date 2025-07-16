from uuid import UUID
from asyncpg import Connection
from fastapi import APIRouter, Depends, Body, Path, HTTPException, status
from typing import Annotated, Any
from app.models import TokenData, StepCreateModel, StepUpdateModel, \
                       TCListMember, TCCreateModel, TCUpdateModel
from app.dependencies import db_conn, get_current_user
from app.logic.tc_logic import TCBase, get_list_of_tc_from_db
from app.logic.steps_logic import create_step, update_neighbours,\
                                  update_step_in_db, delete_step_in_db


tc_router = APIRouter(
    prefix="/test-cases",
    tags=["test-cases"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


#steps    
@tc_router.post('/{id}/steps/')
async def create_new_step(test_case_id: Annotated[UUID, Path(alias='id')],
                    body: Annotated[StepCreateModel, Body()],
                    db_conn: Annotated[Connection, Depends(db_conn)]):
    async with db_conn.transaction():
        try: 
            step_id = await create_step(body, db_conn, test_case_id)
            await update_neighbours(step_id, db_conn, insert=True)
        except ValueError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args)


@tc_router.patch('/steps/{id}')
async def update_step(step_id: Annotated[UUID, Path(alias=('id'))],
                      body: Annotated[StepUpdateModel, Body()],
                    db_conn: Annotated[Connection, Depends(db_conn)]):

    async with db_conn.transaction():
        await update_neighbours(step_id, db_conn, remove=True)
        await update_step_in_db(step_id, db_conn, body)
        await update_neighbours(step_id, db_conn, insert=True)


@tc_router.delete('/steps/{id}')
async def delete_step(step_id: Annotated[UUID, Path(alias=('id'))],
                    db_conn: Annotated[Connection, Depends(db_conn)]):
    async with db_conn.transaction():
        try:
            await update_neighbours(step_id, db_conn, remove=True)
            await delete_step_in_db(step_id, db_conn)
        except ValueError as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, e.args)


#cases       
@tc_router.get('/{id}')#, response_model=TCBase
async def get_tc(test_case_id: Annotated[UUID, Path(alias='id')],
                 db_conn: Annotated[Connection, Depends(db_conn)]):
    try:
        response = await TCBase.get_tc_from_db(test_case_id, db_conn)
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return response


@tc_router.get('/', response_model=list[TCListMember])
async def get_list_of_tc(db_conn: Annotated[Connection, Depends(db_conn)]):
    return await get_list_of_tc_from_db(db_conn)


@tc_router.post('/')#, response_model=TCBase
async def create_tc(body: Annotated[TCCreateModel, Body()], 
                    db_conn: Annotated[Connection, Depends(db_conn)],
                    token_data: Annotated[TokenData, Depends(get_current_user)]):
    try:
        body = body.model_dump()
        response = await TCBase(**body).create_tc(db_conn, 
                                                  token_data.user_id)
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        #log e 
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response


@tc_router.patch('/{id}')#, response_model=TCBase
async def update_test_case(test_case_id: Annotated[UUID, Path(alias='id')],
                           db_conn: Annotated[Connection, Depends(db_conn)],
                           body: Annotated[TCUpdateModel, Body()]):
    await TCBase.update_tc(test_case_id, db_conn, body)


@tc_router.delete('/{id}')
async def delete_tc(test_case_id: Annotated[UUID, Path(alias='id')],
                    db_conn: Annotated[Connection, Depends(db_conn)]):
    try:
        await TCBase.delete_tc(test_case_id, db_conn)
    except ValueError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return 'Test case deleted.'


@tc_router.get('/', response_model=list[TCListMember])
async def get_list_of_tc(db_conn: Annotated[Connection, Depends(db_conn)]):
    return await get_list_of_tc_from_db(db_conn)