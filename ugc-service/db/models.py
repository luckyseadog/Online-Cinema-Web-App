import uuid

from sqlalchemy import UUID, DateTime, String, Float
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Rating(Base):
    __tablename__ = "rating"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    film_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f"Ratings(id={self.id!r}, rating={self.rating!r})"


class Review(Base):
    __tablename__ = "review"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    film_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    review: Mapped[str] = mapped_column(String(5000), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f"Reviews(id={self.id!r}, review={self.review!r})"


class Favourite(Base):
    __tablename__ = "favourite"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    film_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now())

    def __repr__(self) -> str:
        return f"Favourite(id={self.id!r})"
