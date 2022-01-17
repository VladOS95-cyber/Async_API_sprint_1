from typing import List

from models.base import BaseOrjsonModel
from models.film import FilmShortResponse


class PersonShortResponse(BaseOrjsonModel):
    id: str
    full_name: str


class PersonDetailed(BaseOrjsonModel):
    id: str
    full_name: str
    roles: List[str] = []
    films: List[FilmShortResponse] = []


class ReponcePersonDetailed(BaseOrjsonModel):
    id: str
    full_name: str
    roles: List[str] = []
    films: List[FilmShortResponse] = []
