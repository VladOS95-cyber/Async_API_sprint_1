from typing import List, Union

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel): 
      class Config: 
            json_loads = orjson.loads 
            json_dumps = orjson_dumps


class Person(BaseOrjsonModel):
    id: str
    name: str


class InfoFilm(BaseOrjsonModel):
    id: str
    title: str


class Film(BaseOrjsonModel):
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



class Films(BaseOrjsonModel):
    films: List[Film] = []


class ResponceFilm(BaseOrjsonModel):
    id: str
    imdb_rating: Union[float, None] = 0.0
    genre: List[str] = []
    title: str
    description: Union[str, None] = ""
    director: Union[str, None] = ""
    actors_names: List[str] = []
    writers_names: List[str] = []


class ResponceFilms(BaseOrjsonModel):
    films: List[Film] = []
