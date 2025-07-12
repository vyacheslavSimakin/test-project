from fastapi import FastAPI

from app.routers.users import users_router
#from routers.tc_router import tc_router
from app.routers.login import login_router

from contextlib import asynccontextmanager
from app.db.postgress import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    await database.startup()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(login_router)

@app.get('/testing')
def reqtest():
    return "Good job!"