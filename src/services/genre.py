from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import GenreDetailed, Genres

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class GenreService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Optional[GenreDetailed]:
        genre = await self._genre_from_cache(genre_id)
        if not genre:
            genre = await self._get_genre_from_elastic(genre_id)
            if not genre:
                return None
            await self._put_genre_to_cache(genre)
        return genre

    async def get_all_genres(self) -> Genres:
        doc = await self.elastic.get("genres", "_search")
        total_value = doc["hits"]["total"]["value"]
        genres = await self._genres_from_cache("genres")
        if not genres or len(genres.genres) < total_value:
            genres = await self._get_all_genres_from_elastic(total_value)
            if not genres:
                return None
            await self._put_genres_to_cache(genres)
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Optional[GenreDetailed]:
        doc = await self.elastic.get("genres", genre_id)
        return GenreDetailed(**doc["_source"])

    async def _get_all_genres_from_elastic(self, total_value) -> Genres:
        all_results = await self.elastic.search(None, "genres", size=total_value)
        source = [i["_source"] for i in all_results["hits"]["hits"]]
        genres = [GenreDetailed(**genre) for genre in source]
        return Genres(genres=genres)

    async def _genre_from_cache(self, genre_id: str) -> Optional[GenreDetailed]:
        data = await self.redis.get(genre_id)
        if not data:
            return None
        genre = GenreDetailed.parse_raw(data)
        return genre

    async def _genres_from_cache(self, genres) -> Genres:
        data = await self.redis.get(genres)
        if not data:
            return None
        genres = Genres.parse_raw(data)
        return genres

    async def _put_genres_to_cache(self, genres: Genres):
        await self.redis.set(
            "genres", genres.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def _put_genre_to_cache(self, genre: GenreDetailed):
        await self.redis.set(
            genre.id, genre.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
