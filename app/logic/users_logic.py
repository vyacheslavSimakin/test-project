from app.models import UserModel
from app.logic.auth import get_user_by_email, check_user_by_id, \
                           get_password_hash
import logging
logging.getLogger('passlib').setLevel(logging.ERROR)


async def get_user_from_db(user_id, connection):
    user = await connection.fetchrow(f'''SELECT user_id, first_name, 
    last_name FROM users WHERE user_id = {user_id}''')
    if user:
        return UserModel(first_name=user['first_name'], 
                         last_name=user['last_name'], user_id=user_id)
    return None


async def get_users_from_db(connection):
    users = await connection.fetch(f'''SELECT user_id, first_name, 
    last_name FROM users''')
    users = [UserModel(**user) for user in users]
    return users


async def create_user_in_db(body, connection):
    user = dict(body)
    if await get_user_by_email(user['email'], connection):
        raise ValueError
    user['password'] = get_password_hash(user['password'])

    await connection.execute('''INSERT INTO users
    ( role, first_name, last_name, password, email, verified)
    VALUES($1, $2, $3, $4, $5, False); ''', user['role'], user['first_name']
    , user['last_name'], user['password'], user['email'])


async def update_user_in_db(user_id, body, connection):
    user = await check_user_by_id(user_id, connection)
    if user is None: 
        raise ValueError

    body = body.model_dump(exclude_unset=True)
    r = ', '.join(f'{key}=${i}' for i, key in enumerate(body.keys(), 1))
    q = f'UPDATE USERS SET {r} WHERE user_id=${len(body)+1}'
    await connection.execute(q, *body.values(), user_id)


async def delete_user_in_db(user_id, connection):
    user = await connection.fetchrow('''SELECT first_name FROM users WHERE
                               user_id=$1''', user_id)
    if user is None:
        raise ValueError
    await connection.execute('''DELETE FROM users WHERE 
                             user_id=$1''', user_id)