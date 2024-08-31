import enum
import uuid

from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Action(enum.Enum):
    LOGIN = 1
    LOGOUT = 2


user_right = Table(
    "user_right",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
    Column("right_id", ForeignKey("right.id"), primary_key=True),  # pyright: ignore[reportUnknownArgumentType]
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(String(60), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    histories: Mapped[list["History"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    rights: Mapped[list["Right"]] = relationship(secondary=user_right, back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r}, name={self.first_name!r})"


class Right(Base):
    __tablename__ = "right"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    users: Mapped[list[User]] = relationship(secondary=user_right, back_populates="rights")

    def __repr__(self) -> str:
        return f"Right(id={self.id!r}, name={self.name!r})"


class History(Base):
    __tablename__ = "history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("user.id"))
    ip_address: Mapped[str] = mapped_column(String(60), nullable=False)
    action: Mapped[Action] = mapped_column(Integer, nullable=False)
    browser_info: Mapped[str] = mapped_column(String(256), nullable=True)
    system_info: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    user: Mapped[User] = relationship(back_populates="histories")
