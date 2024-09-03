# import http
# from collections.abc import Callable, Coroutine
# from typing import Any

# import pytest
# from sqlalchemy.ext.asyncio.session import AsyncSession

# from src.models_access_control import CreateRightModel, ErrorBody, RightModel
# from testdata.alchemy_model import Right, User


# @pytest.mark.parametrize(
#     ("query_data", "expected_answer"),
#     [
#         (
#             {"name": "subscriber", "right": "admin"},
#             {"status": (http.HTTPStatus.OK, http.HTTPStatus.MISDIRECTED_REQUEST), "length": (3, 1)},
#         ),
#     ],
# )
# @pytest.mark.asyncio(scope="session")
# async def test_creation_of_right(
#     create_database: Callable[[], Coroutine[Any, Any, None]],
#     drop_database: Callable[[], Coroutine[Any, Any, None]],
#     pg_session: AsyncSession,
#     make_post_request: Callable[..., Coroutine[Any, Any, tuple[Any, int]]],
#     query_data: dict[str, str],
#     expected_answer: dict[str, tuple[int, int]],
# ) -> None:
#     # 1. Создаем таблицы в базе данных

#     await create_database()

#     # 2. Создаем юзера и право

#     right_ = Right(name=query_data["right"])
#     user_ = User(
#         login=query_data["right"],
#         password="password",
#         first_name="first_name",
#         last_name="last_name",
#         email="email",
#         rights=[right_],
#     )
#     pg_session.add(right_)
#     pg_session.add(user_)
#     await pg_session.commit()

#     # 2. Генерируем данные

#     right = CreateRightModel(name=query_data["name"])

#     # 3. Создаем право в бд через auth api

#     body, status = await make_post_request("access_control/creation_of_right/", json=right.model_dump())

#     # 4. Проверяем ответ

#     assert status == expected_answer["status"][0]
#     assert len(RightModel(**body).model_dump()) == expected_answer["length"][0]

#     # 5. Пытаемся повторно создать право в бд через auth api

#     body, status = await make_post_request("access_control/creation_of_right/", json=right.model_dump())

#     # 6. Проверяем ответ

#     assert status == expected_answer["status"][1]
#     assert len(ErrorBody(**body).model_dump()) == expected_answer["length"][1]

#     # 7. Стираем таблицы  в базе данных

#     await drop_database()
