from typing import List, Union

import orjson
from pydantic import BaseModel


class InfoFilm(BaseModel):
    id: str
    title: str


class PersonDetailed(BaseModel):
    id: str
    full_name: str
    roles: List[str] = []
    films: List[InfoFilm] = []


class Persons(BaseModel):
    persons: List[PersonDetailed] = []
