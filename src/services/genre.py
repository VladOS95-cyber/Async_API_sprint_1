from functools import lru_cache
from operator import index

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import GenreDetailed
from services.base import BaseService


class GenreService(BaseService):
    pass


@lru_cache()
def get_genre_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(index="genres", model=GenreDetailed, elastic=elastic, redis=redis)
