from sqlalchemy.orm import Session
from core.config import settings
import typer
from typing import Annotated
from sqlalchemy import create_engine
from models.entity import RoleModel, UserModel
from services.password_service import PasswordService

app = typer.Typer()

dsn = (
    f'postgresql://{settings.pg_user}'
    f':{settings.pg_password}@{settings.pg_host}'
    f':{settings.pg_port}/{settings.pg_name}'
)

engine = create_engine(dsn, echo=True, future=True)


def create_superadmin_role(role_title: Annotated[str, typer.Argument()] = 'superadmin'):
    with Session(engine) as session:
        role = RoleModel(title=role_title, description='Superadmin role. All granted')
        session.add(role)
        session.commit()


def create_superadmin_user():
    with Session(engine) as session:
        pass_service = PasswordService()
        superadmin = UserModel(
            login=settings.sa_login,
            email=settings.sa_email,
            first_name=settings.sa_firstname,
            last_name=settings.sa_lastname,
            password=pass_service.compute_hash(settings.sa_password),
            is_superadmin=True,
        )
        session.add(superadmin)
        session.commit()


def assign_superadmin_role_to_superadmin():
    with Session(engine) as session:
        superadmin = session.query(UserModel).filter(UserModel.login == settings.sa_login).first()
        superadmin_role = session.query(RoleModel).filter(RoleModel.title == 'superadmin').first()
        superadmin.roles.append(superadmin_role)
        session.commit()


@app.command()
def create_superadmin():
    create_superadmin_role()
    create_superadmin_user()
    assign_superadmin_role_to_superadmin()


@app.command()
def delete_seperadmin():
    with Session(engine) as session:
        user = session.query(UserModel).where(UserModel.login == settings.sa_login).one()
        session.delete(user)
        session.commit()


if __name__ == '__main__':
    app()
