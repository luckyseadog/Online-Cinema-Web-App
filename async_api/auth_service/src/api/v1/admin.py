from fastapi import status
from db.postgres import AsyncSession, get_session, UserRoleUUID
from fastapi import APIRouter, Depends
from schemas.entity import Role, User
from services.role_service import role_service
from services.user_service import user_service

router = APIRouter()


@router.post(
    '/user_role/assign',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Назначение роли пользователю',
    description='''
    В теле запроса принимает два параметра: uuid пользователя и uuid роли.
    - Если у пользователяю роль присутствует ничего не происходит.\n
    - Если у пользователя нет роли, то она добавляется.\n
    - Если нет такого пользователя возвращается ошибка 404 с описанием что такого пользователя нет.\n
    - Если нет такой роли - возвращаетс ошибка 404 с описаниме, что нет такой роли.\n
    ''',
)
async def assign_role(user_role_uuid: UserRoleUUID, db: AsyncSession = Depends(get_session)) -> User:
    updated_user = await user_service.assing_user_role(user_role_uuid, db)
    return updated_user


@router.post(
    '/user_role/revoke',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Отзыв роли у пользователя',
    description='',
)
async def revoke_role(user_role_uuid: UserRoleUUID, db: AsyncSession = Depends(get_session)) -> User:
    updated_user = await user_service.revoke_user_role(user_role_uuid, db)
    return updated_user


@router.post(
    '/user_role/check',
    status_code=status.HTTP_200_OK,
    summary='Проверка наличия роли у пользователя',
    description='',
)
async def check_role(user_role_uuid: UserRoleUUID, db: AsyncSession = Depends(get_session)):
    res = await user_service.check_user_role(user_role_uuid, db)
    return {'result': 'YES' if res else 'NO'}


@router.get(
    '/roles',
    response_model=list[Role],
    status_code=status.HTTP_200_OK,
    summary='Получение списка ролей',
    description='',
)
async def get_roles(db: AsyncSession = Depends(get_session)) -> list[Role]:
    return await role_service.get_roles(db=db)


@router.post(
    '/roles',
    response_model=Role,
    status_code=status.HTTP_200_OK,
    summary='Добавление роли',
    description='',
)
async def add_role(role_create: Role, db: AsyncSession = Depends(get_session)):
    return await role_service.create_role(db=db, role_create=role_create)


@router.put(
    '/roles',
    #     response_model=,
    status_code=status.HTTP_200_OK,
    summary='Обновление роли',
    description='',
)
async def update_role(role_create: Role, db: AsyncSession = Depends(get_session)):
    return await role_service.update_role(role_create, db=db)


@router.delete(
    '/roles',
    status_code=status.HTTP_200_OK,
    summary='Удаление роли',
    description='',
)
async def delete_role(id: int, db: AsyncSession = Depends(get_session)):
    return await role_service.delete_role(db=db, role_id=id)
