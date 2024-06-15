import json
import time
from api.v1.errors import UserError
from services.token_service import access_token_service


async def validate_token(access_token, refresh_token, redis):
    if access_token is None and refresh_token is None:
        raise UserError('You are not logged in')

    if not access_token_service.validate_token(access_token):
        raise UserError('Invalid access token')

    payload_str = access_token_service.decode_b64(access_token.split('.')[1])
    payload = json.loads(payload_str)

    if await redis.check_banned_atoken(payload['sub'], access_token):
        raise UserError('Access token is banned')

    if payload['exp'] < time.time():
        raise UserError('Access token expired')

    return payload
