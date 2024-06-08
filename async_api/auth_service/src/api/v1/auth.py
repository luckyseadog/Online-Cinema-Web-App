
from fastapi import APIRouter

router = APIRouter()


@router.post('/signup', tags=['auth'])
async def signup():
    return {"message": "signup"}

@router.post('/login', tags=['auth'])
async def login():
    return {"message": "login"}


@router.post('/logout', tags=['auth'])
async def logout():
    return {"message": "logout"}


@router.post('/logout_all', tags=['auth'])
async def logout_all():
    return {"message": "logout_all"}


@router.post('/refresh', tags=['auth'])
async def refresh():
    return {"message": "refresh"}

@router.post('/signup_guest', tags=['auth'])
async def signup_guest():
    return {"message": "signup_guest"}