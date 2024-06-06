from fastapi import FastAPI
import uvicorn
import logging
from contextlib import asynccontextmanager
from core.logger import LOGGING
from fastapi.responses import ORJSONResponse
from enum import Enum

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info('start')
    yield
    logging.info('end')


app = FastAPI(
    title='Сервис аутентификации',
    description='серивис авторизации онлайн кинотеатра',
    version='1.0.0',
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


# USER

@app.get('/api/v1/auth/user/access', tags=['user'])
async def get_access():
    return {"message": "get new tokens"}

@app.delete('/api/v1/auth/user', tags=['user'])
async def delete_user():
    return {"message": "delete user"}


@app.patch('/api/v1/auth/user', tags=['user'])
async def change_user():
    return {"message": "change user"}

@app.get('/api/v1/auth/user/history', tags=['user'])
async def get_history():
    return {"message": "history of user"}


#ADMIN

class Method(str, Enum):
    assign = "assign"
    revoke = "revoke"
    check = "check"


@app.post('/api/v1/auth/admin/user_role/{method}', tags=['admin'])
async def change_role(method: Method):
    return {"message": "change role of a user"}


@app.get('/api/v1/auth/admin/roles/all', tags=['admin'])
async def get_roles():
    return {"message": "roles get"}


@app.post('/api/v1/auth/admin/roles/role', tags=['admin'])
async def add_role():
    return {"message": "roles added"}


@app.patch('/api/v1/auth/admin/roles/role', tags=['admin'])
async def update_role():
    return {"message": "roles update"}


@app.delete('/api/v1/auth/admin/roles/role', tags=['admin'])
async def delete_role():
    return {"message": "roles delete"}


#AUTH

@app.post('/api/v1/auth/signup', tags=['auth'])
async def signup():
    return {"message": "signup"}

@app.post('/api/v1/auth/login', tags=['auth'])
async def login():
    return {"message": "login"}


@app.post('/api/v1/auth/logout', tags=['auth'])
async def logout():
    return {"message": "logout"}


@app.post('/api/v1/auth/logout_all', tags=['auth'])
async def logout_all():
    return {"message": "logout_all"}


@app.post('/api/v1/auth/refresh', tags=['auth'])
async def refresh():
    return {"message": "refresh"}

@app.post('/api/v1/auth/signup_guest', tags=['auth'])
async def signup_guest():
    return {"message": "signup_guest"}


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )