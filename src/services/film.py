from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film, Films

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[Film]:
        film = await self._film_from_cache(film_id)
        if not film:
            film = await self._get_film_from_elastic(film_id)
            if not film:
                return None
            await self._put_film_to_cache(film)
        return film

    async def get_all_films(self) -> Films:
        doc = await self.elastic.get("movies", "_search")
        total_value = doc["hits"]["total"]["value"]
        films = await self._films_from_cache("films")
        if not films or len(films.films) < total_value:
            films = await self._get_all_films_from_elastic(total_value)
            if not films:
                return None
            await self._put_films_to_cache(films)
        return films

    async def _get_film_from_elastic(self, film_id: str) -> Optional[Film]:
        doc = await self.elastic.get("movies", film_id)
        return Film(**doc["_source"])

    async def _get_all_films_from_elastic(self, total_value) -> Films:
        all_results = await self.elastic.search(None, "movies", size=total_value)
        source = [i["_source"] for i in all_results["hits"]["hits"]]
        films = [Film(**film) for film in source]
        return Films(films=films)

    async def _film_from_cache(self, film_id: str) -> Optional[Film]:
        data = await self.redis.get(film_id)
        if not data:
            return None
        film = Film.parse_raw(data)
        return film

    async def _films_from_cache(self, films) -> Films:
        data = await self.redis.get(films)
        if not data:
            return None
        film = Films.parse_raw(data)
        return film

    async def _put_films_to_cache(self, films: Films):
        await self.redis.set("films", films.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)

    async def _put_film_to_cache(self, film: Film):
        await self.redis.set(film.id, film.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS)


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
