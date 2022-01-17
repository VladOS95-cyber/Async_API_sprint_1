from typing import List, Union

from models.base import BaseOrjsonModel
from models.film import FilmShortResponse


class GenreShortResponse(BaseOrjsonModel):
    id: str
    name: str
    description: Union[str, None] = ""


class GenreDetailed(BaseOrjsonModel):
    id: str
    name: str
    description: Union[str, None] = ""
    films: List[FilmShortResponse] = []


class ResponceGenreDetailed(BaseOrjsonModel):
    id: str
    name: str
    description: Union[str, None] = ""
    films: List[FilmShortResponse] = []
