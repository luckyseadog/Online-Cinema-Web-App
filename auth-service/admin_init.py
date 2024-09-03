import typer
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models.alchemy_model import Right, User
from services.password_service import get_password_service
from core.config import configs, admin_config


engine = create_engine(configs.postgres_dsn)
ps = get_password_service()
app = typer.Typer()


def create_admin_right(session: Session) -> Right:
    admin_right = session.scalars(select(Right).where(Right.name == admin_config.right_name)).first()
    if admin_right:
        raise typer.Exit
    else:
        admin_right = Right(
            name=admin_config.right_name,
            description="admin right allows everything"
        )
        session.add(admin_right)

    return admin_right


def creaete_admin_user(session: Session) -> User:
    admin_user = session.scalars(select(User).where(User.login == admin_config.username)).first()
    if admin_user:
        raise typer.Exit
    else:
        admin_user = User(
            login=admin_config.username,
            password=ps.compute_hash(admin_config.password),
            first_name=admin_config.first_name,
            last_name=admin_config.last_name,
            email=admin_config.email,
        )
        session.add(admin_user)

    return admin_user


@app.command()
def create_admin() -> None:
    with Session(engine) as pg_session:
        admin_right = create_admin_right(pg_session)
        admin_user = creaete_admin_user(pg_session)
        admin_user.rights.append(admin_right)
        pg_session.commit()


@app.command()
def delete_admin() -> None:
    with Session(engine) as session:
        admin_right = session.scalars(select(Right).where(Right.name == admin_config.right_name)).first()
        session.delete(admin_right)
        admin_user = session.scalars(select(User).where(User.login == admin_config.username)).first()
        session.delete(admin_user)
        session.commit()


if __name__ == "__main__":
    app()
