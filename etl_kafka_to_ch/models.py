from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class Event(BaseModel):
    user_id: UUID = Field(description="UUID")
    movie_id: str | None = Field(description="String NULL")
    prev_qual: int | None = Field(description="int NULL")
    new_qual: int | None = Field(description="int NULL")
    element_id: str | None = Field(description="String NULL")
    group_id: str | None = Field(description="String NULL")
    time: str | None = Field(description="String NULL")
    action: Literal["add", "remove", "stop", "pause"] | None = Field(
        description="Enum('add', 'remove', 'stop', 'pause') NULL"
    )
    feedback: str | None = Field(description="String NULL")
    rating: int | None = Field(description="int NULL")
    filter_id_genre: list[str] | None = Field(description="Array(String) NULL")
    filter_rating: int | None = Field(description="int NULL")
    filter_id_actor: list[str] | None = Field(description="Array(String) NULL")
    film_curr_time: int | None = Field(description="int NULL")
    film_abs_time: int | None = Field(description="int NULL")
    url: str | None = Field(description="String NULL")
    spent_time: int | None = Field(description="int NULL")
