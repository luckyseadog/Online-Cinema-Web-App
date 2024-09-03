import os

import typer
from dotenv import load_dotenv
from sqlalchemy import create_engine, delete, select
from sqlalchemy.orm import Session

from models.alchemy_model import Right, User
from services.password_service import get_password_service

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

engine = create_engine(f"postgresql+psycopg://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
ps = get_password_service()
app = typer.Typer()


def create_admin_right(session: Session):
    admin_right = session.scalars(select(Right).where(Right.name == "admin")).first()
    if admin_right:
        raise typer.Exit()
    else:
        admin_right = Right(
            name="admin",
            description="admin right allows everything"
        )
        session.add(admin_right)

    return admin_right


def creaete_admin_user(session: Session):
    admin_user = session.scalars(select(User).where(User.login == "admin")).first()
    if admin_user:
        raise typer.Exit()
    else:
        admin_user = User(
            login="admin",
            password=ps.compute_hash("ADMIN_PASSWORD"),
            first_name="admin",
            last_name="admin",
            email="admin@gmail.com",
        )
        session.add(admin_user)

    return admin_user


@app.command()
def create_admin():
    with Session(engine) as pg_session:
        admin_right = create_admin_right(pg_session)
        admin_user = creaete_admin_user(pg_session)
        admin_user.rights.append(admin_right)
        pg_session.commit()


@app.command()
def delete_admin():
    with Session(engine) as pg_session:
        pg_session.execute(delete(User).where(User.login == "admin"))
        pg_session.execute(delete(Right).where(Right.name == "admin"))
        pg_session.commit()


if __name__ == "__main__":
    app()
