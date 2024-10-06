from typing import Literal
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


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
    filter_id_genre: list[str] | None = Field(description="Array(String)")
    filter_rating: int | None = Field(description="int NULL")
    filter_id_actor: list[str] | None = Field(description="Array(String)")
    film_curr_time: int | None = Field(description="int NULL")
    film_abs_time: int | None = Field(description="int NULL")
    url: str | None = Field(description="String NULL")
    spent_time: int | None = Field(description="int NULL")
    timestamp: datetime = Field(description="DateTime", default_factory=datetime.now)

    @field_validator("filter_id_genre", "filter_id_actor")
    @classmethod
    def validate_x(cls, v: list[str] | None) -> list[str]:
        return [] if v is None else v
