from fastapi import FastAPI
import uvicorn
import logging
from contextlib import asynccontextmanager
from core.logger import LOGGING
from fastapi.responses import ORJSONResponse

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

@app.get('/api/v1/auth/me', tags=['me'])
async def get_me():
    return {"message": "me get"}

@app.patch('/api/v1/auth/me', tags=['me'])
async def get_me():
    return {"message": "me patch"}

@app.delete('/api/v1/auth/me', tags=['me'])
async def get_me():
    return {"message": "me delete"}

@app.post('/api/v1/auth/admin/roles/assign', tags=['admin'])
async def assign_roles():
    return {"message": "roles assign"}


@app.post('/api/v1/auth/admin/roles/revoke', tags=['admin'])
async def revoke_roles():
    return {"message": "roles revoke"}


@app.post('/api/v1/auth/admin/roles/check', tags=['admin'])
async def assign_permissions():
    return {"message": "check role"}


@app.get('/api/v1/auth/me/history', tags=['me'])
async def get_history():
    return {"message": "history get"}


@app.post('/api/v1/auth/signin', tags=['auth'])
async def signin():
    return {"message": "signin"}


@app.post('/api/v1/auth/signout', tags=['auth'])
async def signout():
    return {"message": "signout"}


@app.post('/api/v1/auth/signout_all', tags=['auth'])
async def sugnout_all():
    return {"message": "signout_all"}


@app.post('/api/v1/auth/signup', tags=['auth'])
async def signup():
    return {"message": "signup"}


@app.post('/api/v1/auth/refresh', tags=['auth'])
async def refresh():
    return {"message": "refresh"}


@app.get('/api/v1/auth/admin/roles', tags=['admin'])
async def get_roles():
    return {"message": "roles get"}


@app.post('/api/v1/auth/admin/roles', tags=['admin'])
async def add_roles():
    return {"message": "roles added"}


@app.patch('/api/v1/auth/admin/roles', tags=['admin'])
async def update_roles():
    return {"message": "roles update"}


@app.delete('/api/v1/auth/admin/roles', tags=['admin'])
async def delete_roles():
    return {"message": "roles delete"}


if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )