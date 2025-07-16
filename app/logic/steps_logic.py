from uuid import UUID, uuid4
from asyncpg import Connection
from fastapi import HTTPException, status
from app.models import Step, StepCreateModel, StepUpdateModel 


async def get_step_from_db(step_id: UUID, connection: Connection):
    step = await connection.fetchrow('''SELECT step_id, description, 
                        expected_result, next_step_id, prev_step_id 
                        FROM steps WHERE step_id=$1''', step_id)
    if step is None: raise HTTPException(status.HTTP_404_NOT_FOUND)
    return StepUpdateModel(**step)


async def delete_step_in_db(step_id: UUID, connection: Connection):
    step = await get_step_from_db(step_id, connection)
    if not step.next_step_id and not step.prev_step_id:
            raise ValueError("Can't delete step. Test case must contain at least one step.")

    await connection.execute('DELETE FROM steps WHERE step_id = $1', step_id)


async def create_step(step: StepCreateModel, connection: Connection, 
                      test_case_id: uuid4):
    if not step.prev_step_id and not step.next_step_id: 
        raise ValueError("Unable to create new step. Must provide next_step_id or prev_step_id")
    #to do: if tc id in the prev or next step is different: raise
    step_id = uuid4()
    await connection.execute('''INSERT INTO steps (step_id,
        description, expected_result, next_step_id, prev_step_id,
        test_case_id) VALUES($1, $2, $3, $4, $5, $6);''', step_id, 
        step.description, step.expected_result, step.next_step_id, 
        step.prev_step_id, test_case_id)
    return step_id


async def update_neighbours(step_id:UUID, connection: Connection, 
                            insert: bool=False, remove: bool=False) -> None:
    if not insert and not remove: raise ValueError('insert or remove must be selected')
    next_step_update_query = 'UPDATE steps SET next_step_id=$1 WHERE step_id=$2'
    prev_step_update_query = 'UPDATE steps SET prev_step_id=$1 WHERE step_id=$2'
    
    step = await get_step_from_db(step_id, connection)
    prev_step_id = step.prev_step_id
    next_step_id = step.next_step_id


    if insert:
        if prev_step_id and next_step_id:
            await connection.execute(prev_step_update_query, step_id, 
                                     next_step_id)
            await connection.execute(next_step_update_query, step_id, 
                                     prev_step_id)
        elif prev_step_id:
            await connection.execute(next_step_update_query, step_id, 
                                     prev_step_id)
        elif next_step_id:
            await connection.execute(prev_step_update_query, step_id, 
                                     next_step_id)
    
    elif remove:
        if next_step_id and prev_step_id:
            await connection.execute(next_step_update_query,
                                     next_step_id, prev_step_id)
            await connection.execute(prev_step_update_query,
                                     prev_step_id, next_step_id)
        elif prev_step_id:
            await connection.execute(next_step_update_query,
                                     next_step_id, prev_step_id)
        elif next_step_id:
            await connection.execute(prev_step_update_query,
                                     prev_step_id, next_step_id)


async def update_step_in_db(step_id: UUID, connection: Connection, 
                            body: StepUpdateModel):
    await get_step_from_db(step_id, connection)
    
    new_body = body.model_dump(exclude_unset=True)
    if body.prev_step_id or body.next_step_id:
        if 'prev_step_id' not in new_body: new_body['prev_step_id'] = None 
        if 'next_step_id' not in new_body: new_body['next_step_id'] = None 
    r = ', '.join(f'{key}=${i}' for i, key in enumerate(new_body.keys(), 1))
    q = f'UPDATE steps SET {r} WHERE step_id=${len(new_body)+1}'
    await connection.execute(q, *new_body.values(), step_id)