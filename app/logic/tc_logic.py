from pydantic import Field
from typing import Self
from uuid import UUID, uuid4
from asyncpg import Connection
from app.models import Step, TCCreateModel, TCUpdateModel, TCListMember
    

#to do get list of steps
class TCBase(TCCreateModel):
    steps: dict[int, Step] | None = None 
    test_case_id: UUID = Field(default_factory=uuid4) 
    created_by: int | None = None


    async def create_tc(self, connection: Connection, created_by):
        """Stores new test case in db, along with empty step.

        Args:
            connection (Connection): Db connection.
            created_by (_type_): Author of test case.
        """
        async with connection.transaction():
            self.created_by = created_by
            await connection.execute('''INSERT INTO test_cases
            (test_case_id, name, description, pre_conditions, priority, 
            project_id, created_by) VALUES($1, $2, $3, $4, $5, $6, $7);''', 
            self.test_case_id, self.name, self.description, self.pre_conditions,
            self.priority.value, self.project_id, created_by)

            step_id = uuid4()    
            await connection.execute('''INSERT INTO steps 
            (step_id, description, expected_result, next_step_id, prev_step_id,
            test_case_id) VALUES($1, $2, $3, $4, $5, $6);''', 
            step_id, None, None, None, None, self.test_case_id)
            self.steps = {1:Step(step_id=step_id, description='')}

        return self


    @classmethod
    async def get_tc_from_db(cls, test_case_id: UUID, 
                             connection: Connection) -> Self:
        """Factory for creating test case from test case id.
        Pulls steps of test case as a part of test case.

        Args:
            connection (Connection): Db conenction.
            item_id (UUID): Test case id.

        Returns:
            Self: Instance of TCBase class.
        """
        tc = await connection.fetchrow('''SELECT * FROM test_cases WHERE 
                                       test_case_id = $1''', test_case_id)
        if not tc: raise ValueError
        
        recursive_steps_select_query = '''WITH RECURSIVE list_traversal AS (
                -- Start with the head of the list 
                SELECT step_id, description, expected_result,
                next_step_id, 1 AS position
                FROM steps
                WHERE prev_step_id IS NULL AND test_case_id = $1

                UNION ALL

                -- Recursively find the next node
                SELECT s.step_id, s.description, s.expected_result,
                s.next_step_id, lt.position +1
                from steps s
                JOIN list_traversal lt ON s.step_id = lt.next_step_id
            )
            SELECT step_id, description, expected_result, position
            FROM list_traversal
            ORDER BY position;'''
        
        steps = await connection.fetch(recursive_steps_select_query, 
                                       test_case_id)
        if not steps: raise ValueError

        steps = {step[-1]:Step(step_id=step[0], description=step[1],
                                expected_result=step[2]) for step in steps}
        return cls(steps=steps, **tc)
    

    @staticmethod
    async def check_tc_in_db(test_case_id: UUID, connection: Connection)->bool:
        if await connection.fetchrow('''SELECT name FROM test_cases WHERE 
                                         test_case_id = $1''', test_case_id):
            return True
        return False


    @staticmethod
    async def update_tc(test_case_id: UUID, connection: Connection,
                         body: TCUpdateModel) -> None:
        if not await TCBase.check_tc_in_db(test_case_id, connection):
            raise ValueError

        
        body = body.model_dump(exclude_unset=True)
        body['priority'] = body['priority'].value 
        r = ', '.join(f'{key}=${i}' for i, key in enumerate(body.keys(), 1))
        q = f'UPDATE test_cases SET {r} WHERE test_case_id=${len(body)+1}'
        await connection.execute(q, *body.values(), test_case_id)


    @staticmethod
    async def delete_tc(test_case_id: UUID, connection: Connection) -> None:
        """Deletes test case and all related steps.

        Args:
            item_id (UUID): Test case id.
            connection (Connection): Db connection.
        """
        if not await TCBase.check_tc_in_db(test_case_id, connection):
            raise ValueError
        
        async with connection.transaction():
            await connection.execute('''DELETE FROM steps WHERE 
                                     test_case_id = $1;''', test_case_id)
            await connection.execute('''DELETE FROM test_cases WHERE 
                                     test_case_id = $1;''', test_case_id)
            

async def get_list_of_tc_from_db(connection: Connection) -> list[TCListMember]:
    response = await connection.fetch('''SELECT test_case_id, name, 
                                      priority FROM test_cases''')
    response = [TCListMember(**tc) for tc in response]
    return response