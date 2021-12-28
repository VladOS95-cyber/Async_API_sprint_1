import orjson
from typing import List, Union

from pydantic import BaseModel

def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()

class Person(BaseModel):
    id: str
    name: str


class Film(BaseModel):
    id: str
    imdb_rating: Union[float, None] = 0.0
    genre: List[str] = []
    title: str
    description: Union[str, None] = ""
    director: Union[str, None] = ""
    actors_names: List[str] = []
    writers_names: List[str] = []
    actors: List[Person] = []
    writers: List[Person] = []

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class Films(BaseModel):
    films: List[Film] = []
