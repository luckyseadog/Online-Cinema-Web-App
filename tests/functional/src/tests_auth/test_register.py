# import http
# from collections.abc import Callable, Coroutine
# from http.cookies import SimpleCookie
# from typing import Any

# import pytest

# from core.settings import test_settings
# from src.models_auth import AccountModel


# @pytest.mark.parametrize(
#     ("query_data", "expected_answer"),
#     [
#         ({"login": "register"}, {"status": (http.HTTPStatus.OK, http.HTTPStatus.CONFLICT), "length": (4, 1)}),
#     ],
# )
# @pytest.mark.asyncio(scope="session")
# async def test_register(
#     create_database: Callable[[], Coroutine[Any, Any, None]],
#     drop_database: Callable[[], Coroutine[Any, Any, None]],
#     make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int, SimpleCookie]]],
#     query_data: dict[str, str],
#     expected_answer: dict[str, tuple[int, int]],
# ) -> None:
#     # 1. Создаем таблицы в базе данных

#     await create_database()

#     # 2. Генерируем данные

#     account = AccountModel(
#         login=query_data["login"],
#         password="password",
#         first_name="first_name",
#         last_name="last_name",
#         email="email",
#     )

#     # 3. Создаем аккаунт в бд через auth api

#     body, status, _ = await make_post_request(
#         url=f"{test_settings.service_url_auth}auth/v1/auth/register/", json=account.model_dump()
#     )

#     # 4. Проверяем ответ

#     assert status == expected_answer["status"][0]
#     assert len(body) == expected_answer["length"][0]

#     # 5. Пытаемся повторно создать аккаунт в бд через auth api

#     body, status, _ = await make_post_request(
#         url=f"{test_settings.service_url_auth}auth/v1/auth/register/", json=account.model_dump()
#     )

#     # 6. Проверяем ответ

#     assert status == expected_answer["status"][1]
#     assert len(body) == expected_answer["length"][1]

#     # 7. Стираем таблицы  в базе данных

#     await drop_database()
