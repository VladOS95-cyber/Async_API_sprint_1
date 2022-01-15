from typing import List

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel): 
      class Config: 
            json_loads = orjson.loads 
            json_dumps = orjson_dumps


class InfoFilm(BaseOrjsonModel):
    id: str
    title: str


class PersonDetailed(BaseOrjsonModel):
    id: str
    full_name: str
    roles: List[str] = []
    films: List[InfoFilm] = []


class Persons(BaseOrjsonModel):
    persons: List[PersonDetailed] = []


class ReponcePersonDetailed(BaseOrjsonModel):
    id: str
    full_name: str
    roles: List[str] = []
    films: List[InfoFilm] = []


class ResponcePersons(BaseOrjsonModel):
    persons: List[PersonDetailed] = []
