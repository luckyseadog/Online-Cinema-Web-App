import enum
import uuid

from sqlalchemy import JSON, UUID, Boolean, Column, DateTime, Enum, ForeignKey, Index, String, Table
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declared_attr
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Action(enum.Enum):
    LOGIN = 1
    LOGOUT = 2


user_right = Table(
    "user_right",
    Base.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("right_id", ForeignKey("right.id", ondelete="CASCADE"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    password: Mapped[tuple[str, int, str, str]] = mapped_column(JSON, nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    email: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    histories: Mapped[list["History"]] = relationship(
        back_populates="user", cascade="all, delete-orphan", lazy="selectin"
    )
    rights: Mapped[list["Right"]] = relationship(secondary=user_right, back_populates="users", lazy="selectin")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, login={self.login!r}, name={self.first_name!r})"


class Right(Base):
    __tablename__ = "right"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(60), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())
    modified_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    users: Mapped[list[User]] = relationship(secondary=user_right, back_populates="rights", lazy="selectin")

    def __repr__(self) -> str:
        return f"Right(id={self.id!r}, name={self.name!r})"


class HistoryMixin:
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    ip_address: Mapped[str] = mapped_column(String(60), nullable=False)
    action: Mapped[Action] = mapped_column(Enum(Action), nullable=False)
    browser_info: Mapped[str] = mapped_column(String(256), nullable=True)
    system_info: Mapped[str] = mapped_column(String(256), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    @declared_attr.directive
    def __table_args__(cls):
        return (Index(f"_idx_{cls.__tablename__}", "user_id", "action"),)


class History(HistoryMixin, Base):
    __tablename__ = "history"
    __table_args__ = ({"postgresql_partition_by": "RANGE (created_at)"},)

    user: Mapped[User] = relationship(back_populates="histories", lazy="selectin")


class History2024(HistoryMixin, Base):
    """Partition of history"""

    __tablename__ = "history_2024"


class History2025(HistoryMixin, Base):
    """Partition of history"""

    __tablename__ = "history_2025"


class History2026(HistoryMixin, Base):
    """Partition of history"""

    __tablename__ = "history_2026"


class History2027(HistoryMixin, Base):
    """Partition of history"""

    __tablename__ = "history_2027"
