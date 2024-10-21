import uuid

from sqlalchemy import UUID, Date, DateTime, Double, Float, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class BaseAdmin(DeclarativeBase):
    pass


class BaseUGC(DeclarativeBase):
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


class Rating(BaseUGC):
    __tablename__ = "rating"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    film_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f"Ratings(id={self.id!r}, rating={self.rating!r})"


class Review(BaseUGC):
    __tablename__ = "review"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    film_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    review: Mapped[str] = mapped_column(String(5000), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f"Reviews(id={self.id!r}, review={self.review!r})"


class Favourite(BaseUGC):
    __tablename__ = "favourite"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    film_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f"Favourite(id={self.id!r})"
