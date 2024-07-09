# import pytest
# from tests.functional.settings import auth_test_settings
# from pathlib import Path
# from aiohttp import FormData

# HEADERS = {"Origin": "www.somesite.com"}


# @pytest.mark.asyncio
# async def test_admin_basic(aiohttp_client):
#     data = FormData()
#     data.add_field('username', 'superadmin')
#     data.add_field('password', 'admin')

#     resp = await aiohttp_client.post("/login", data=data)

#     assert resp.status == 200


    # username: john, password: securepassword123


# @pytest.mark.asyncio
# async def test_assign_role(client):
#     response = await client.post('/admin/user_role/assign')
#     assert response.status_code == codes.UNAUTHORIZED


# @pytest.mark.asyncio
# async def test_revoke_role(client):
#     response = await client.post('/admin/user_role/revoke')
#     assert response.status_code == codes.UNAUTHORIZED


# @pytest.mark.asyncio
# async def test_check_role(client):
#     response = await client.post('/admin/user_role/check')
#     assert response.status_code == codes.UNAUTHORIZED
