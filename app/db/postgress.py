import asyncpg
from os import getenv
from dotenv import load_dotenv 

load_dotenv()


class Postgres:
    def __init__(self):
        self.PG_USER = getenv('PG_USER')
        self.PG_PASSWORD = getenv('PG_PASSWORD')
        self.PG_URL = getenv('PG_URL')
        self.PG_PORT = getenv('PG_PORT')
        self.PG_DB = getenv('PG_DB')

    async def connect(self):
        self.pool = await asyncpg.create_pool(user=self.PG_USER, 
                                    password=self.PG_PASSWORD,
                                    database=self.PG_DB, 
                                    host=self.PG_URL,
                                    port=self.PG_PORT,
                                    server_settings={'search_path': "public"})#schema


    async def disconnect(self):
        await self.pool.close()

    async def startup(self):
        #await self.pool.fetch("Select * from public.users")
        #check connection
        #log db connected
        await self.pool.execute('CREATE TABLE IF NOT EXISTS "users" ( \
        "user_id" serial NOT NULL,  \
        "role" varchar(64) NOT NULL, \
        "first_name" varchar(128) NOT NULL, \
        "last_name" varchar(128) NOT NULL, \
        "password" varchar(255) NOT NULL, \
        "email" varchar(255) NOT NULL, \
        "verified" boolean NOT NULL, \
        PRIMARY KEY ("user_id") \
        );')#create tables
        print("startup finished")
        #log db tables created
    
    #async def read(self, what:str, from_:str, where:str=1):
    #    async with self.pool.acquire() as connection:
    #        yield connection.fetch(f"""SELECT {what} FROM {from_} WHERE {where} """)
        
    def __repr__(self) -> str:
        return 'Postgres()'
        

database = Postgres()

