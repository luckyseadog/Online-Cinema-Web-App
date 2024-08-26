from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean
from datetime import datetime
import enum


class Base(DeclarativeBase):
    pass

class Action(enum.Enum):
    LOGIN = 1
    LOGOUT = 2

user_right = Table(
    "user_right",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("right_id", ForeignKey("right.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    modified_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    histories: Mapped[List["History"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    rights: Mapped[List["Right"]] = relationship(
        secondary=user_right, back_populates="users"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r}, name={self.first_name!r})"

class Right(Base):
    __tablename__ = "right"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] =  mapped_column(String(60), unique=True, nullable=False, index=True)
    description: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)
    modified_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    users: Mapped[List[User]] = relationship(
        secondary=user_right, back_populates="rights"
    )

    def __repr__(self) -> str:
        return f"Right(id={self.id!r}, name={self.name!r})"
    

class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("user.id"))
    ip_address: Mapped[str]
    action: Mapped[Action] = mapped_column(Integer, nullable=False)
    browser_info: Mapped[str]
    system_info: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="histories")