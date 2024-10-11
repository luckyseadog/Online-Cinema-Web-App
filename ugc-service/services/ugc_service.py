from collections.abc import Sequence
from functools import lru_cache
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from db.models import Favourite, Rating, Review
from db.postgres_db import get_session


class UGCService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_ratings(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Rating]:
        stmt = select(Rating)
        if user_id:
            stmt = stmt.where(Rating.user_id == user_id)
        if film_id:
            stmt = stmt.where(Rating.film_id == film_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_reviews(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Review]:
        stmt = select(Review)
        if user_id:
            stmt = stmt.where(Review.user_id == user_id)
        if film_id:
            stmt = stmt.where(Review.film_id == film_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_favourites(self, user_id: UUID | None, film_id: UUID | None) -> Sequence[Favourite]:
        stmt = select(Favourite)
        if user_id:
            stmt = stmt.where(Favourite.user_id == user_id)
        if film_id:
            stmt = stmt.where(Favourite.film_id == film_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()


@lru_cache
def get_ugc_service(postgres: Annotated[AsyncSession, Depends(get_session)]) -> UGCService:
    return UGCService(postgres)
