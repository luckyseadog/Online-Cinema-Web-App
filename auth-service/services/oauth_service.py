import aiohttp
from fastapi import HTTPException, status
from functools import lru_cache


class OauthService:
    async def get_user_data_google(self, data: dict[str, str]) -> dict[str, str]:
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with session.post("https://oauth2.googleapis.com/token", data=data, headers=headers) as resp:
                tokens = await resp.json()

            access_token = tokens.get("access_token")
            if not access_token:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=tokens)

            headers = {"Authorization": f"Bearer {access_token}"}
            async with session.get("https://www.googleapis.com/oauth2/v2/userinfo?alt=json", headers=headers) as resp:
                user_data = await resp.json()
        
        return user_data

    async def get_user_data_yandex(self, data: dict[str, str]) -> dict[str, str]:
        async with aiohttp.ClientSession() as session:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            async with session.post("https://oauth.yandex.ru/token", data=data, headers=headers) as resp:
                tokens = await resp.json()

            access_token = tokens.get("access_token")
            if not access_token:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=tokens)

            headers = {"Authorization": f"Bearer {access_token}"}
            async with session.get("https://login.yandex.ru/info?alt=json", headers=headers) as resp:
                user_data = await resp.json()
        
        return user_data


@lru_cache
def get_oauth_service() -> OauthService:
    return OauthService()
