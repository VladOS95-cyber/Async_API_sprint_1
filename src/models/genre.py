from typing import List, Union

import orjson
from pydantic import BaseModel

from models.person import InfoFilm


class GenreDetailed(BaseModel):
    id: str
    name: str
    description: Union[str, None] = ""
    films: List[InfoFilm] = []


class Genres(BaseModel):
    genres: List[GenreDetailed] = []
