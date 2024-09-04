import typer
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from models.alchemy_model import Right, User
from services.password_service import get_password_service
from core.config import configs, admin_config
from sqlalchemy import or_


engine = create_engine(configs.postgres_dsn)
ps = get_password_service()
app = typer.Typer()


def create_admin_right(session: Session) -> Right:
    admin_right = session.scalars(select(Right).where(Right.name == admin_config.right_name)).first()
    if admin_right:
        raise typer.Exit
    else:
        admin_right = Right(name=admin_config.right_name, description="admin right allows everything")
        session.add(admin_right)

    return admin_right


def creaete_admin_user(
    session: Session, 
    name: str | None = None, 
    password: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None, 
) -> User:
    name = name or admin_config.username
    password = ps.compute_hash(password) if password else ps.compute_hash(admin_config.password)
    first_name = first_name or admin_config.first_name
    last_name = last_name or admin_config.last_name
    email = email or admin_config.email

    admin_user = session.scalars(
        select(User).where(
            or_(
                User.login == name,
                User.email == email,
            )
        )
    ).first()

    if admin_user:
        raise typer.Exit
    else:
        admin_user = User(
            login=name,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        session.add(admin_user)

    return admin_user


@app.command()
def create_admin(
    name: str | None = None, 
    password: str | None = None, 
    first_name: str | None = None,
    last_name: str | None = None,
    email: str | None = None, 
) -> None:
    with Session(engine) as pg_session:
        admin_right = pg_session.scalars(select(Right).where(Right.name == admin_config.right_name)).first()
        if not admin_right:
            admin_right = create_admin_right(pg_session)
        admin_user = creaete_admin_user(
            pg_session,
            name,
            password,
            first_name,
            last_name,
            email,
        )
        admin_user.rights.append(admin_right)
        pg_session.commit()


@app.command()
def delete_admin(name: str | None = None) -> None:
    name = name or admin_config.username
    with Session(engine) as session:
        admin_right = session.scalars(select(Right).where(Right.name == admin_config.right_name)).first()
        num_admins = len(session.execute(select(User).where(User.rights.contains(admin_right))).all())
        admin_user = session.scalars(select(User).where(User.login == name)).first()
        if not admin_user:
            raise typer.Exit
        if num_admins == 1:
            session.delete(admin_right)
            session.delete(admin_user)
            session.commit()
        else:
            session.delete(admin_user)
            session.commit()


if __name__ == "__main__":
    app()
