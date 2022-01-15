from typing import List, Union

import orjson
from pydantic import BaseModel

from models.person import InfoFilm


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel): 
      class Config: 
            json_loads = orjson.loads 
            json_dumps = orjson_dumps


class GenreDetailed(BaseOrjsonModel):
    id: str
    name: str
    description: Union[str, None] = ""
    films: List[InfoFilm] = []


class Genres(BaseOrjsonModel):
    genres: List[GenreDetailed] = []


class ResponceGenreDetailed(BaseOrjsonModel):
    id: str
    name: str
    description: Union[str, None] = ""
    films: List[InfoFilm] = []


class ResponceGenres(BaseOrjsonModel):
    genres: List[GenreDetailed] = []
