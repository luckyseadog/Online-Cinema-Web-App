from functools import lru_cache


class MovieService:
    async def get_new_movies(self) -> list[str]:
        return ["The Last Samurai", "Star Wars", "Gone with the Wind"]


@lru_cache
def get_movie_service() -> MovieService:
    return MovieService()
