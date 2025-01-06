import uuid

from sqlalchemy import UUID, Date, DateTime, Double, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class BaseAdmin(DeclarativeBase):
    pass


class FilmWork(BaseAdmin):
    __tablename__ = "film_work"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    creation_date: Mapped[DateTime] = mapped_column(Date(), nullable=True)
    file_path: Mapped[str] = mapped_column(String(), nullable=False)
    rating: Mapped[float] = mapped_column(Double(), nullable=True)
    type: Mapped[str] = mapped_column(String(7), nullable=False)
    created: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    modified: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False, onupdate=func.now())

    __table_args__ = {"schema": "content"}
