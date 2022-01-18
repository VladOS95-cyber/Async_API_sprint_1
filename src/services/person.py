from functools import lru_cache
from typing import Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends

from db.elastic import get_elastic
from db.redis import get_redis
from models.person import PersonDetailed, Persons

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class PersonService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Optional[PersonDetailed]:
        person = await self._person_from_cache(person_id)
        if not person:
            person = await self._get_person_from_elastic(person_id)
            if not person:
                return None
            await self._put_person_to_cache(person)
        return person

    async def get_all_persons(self) -> Persons:
        doc = await self.elastic.get("persons", "_search")
        total_value = doc["hits"]["total"]["value"]
        persons = await self._persons_from_cache("persons")
        if not persons or len(persons.persons) < total_value:
            persons = await self._get_all_persons_from_elastic(total_value)
            if not persons:
                return None
            await self._put_persons_to_cache(persons)
        return persons

    async def _get_person_from_elastic(
        self, person_id: str
    ) -> Optional[PersonDetailed]:
        doc = await self.elastic.get("persons", person_id)
        return PersonDetailed(**doc["_source"])

    async def _get_all_persons_from_elastic(self, total_value) -> Persons:
        all_results = await self.elastic.search(None, "persons", size=total_value)
        source = [i["_source"] for i in all_results["hits"]["hits"]]
        persons = [PersonDetailed(**person) for person in source]
        return Persons(persons=persons)

    async def _person_from_cache(self, person_id: str) -> Optional[PersonDetailed]:
        data = await self.redis.get(person_id)
        if not data:
            return None
        person = PersonDetailed.parse_raw(data)
        return person

    async def _persons_from_cache(self, persons) -> Persons:
        data = await self.redis.get(persons)
        if not data:
            return None
        persons = Persons.parse_raw(data)
        return persons

    async def _put_persons_to_cache(self, persons: Persons):
        await self.redis.set(
            "persons", persons.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def _put_person_to_cache(self, person: PersonDetailed):
        await self.redis.set(
            person.id, person.json(), expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )


@lru_cache()
def get_person_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
