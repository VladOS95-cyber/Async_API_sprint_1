from typing import List, Union

from models.base import BaseOrjsonModel


class PersonShortResponseForFilm(BaseOrjsonModel):
    id: str
    name: str


class FilmShortResponse(BaseOrjsonModel):
    id: str
    title: str


class FilmDetailed(BaseOrjsonModel):
    id: str
    imdb_rating: Union[float, None] = 0.0
    genre: List[str] = []
    title: str
    description: Union[str, None] = ""
    director: Union[str, None] = ""
    actors_names: List[str] = []
    writers_names: List[str] = []
    actors: List[PersonShortResponseForFilm] = []
    writers: List[PersonShortResponseForFilm] = []


class ResponceFilm(BaseOrjsonModel):
    id: str
    imdb_rating: Union[float, None] = 0.0
    genre: List[str] = []
    title: str
    description: Union[str, None] = ""
    director: Union[str, None] = ""
    actors_names: List[str] = []
    writers_names: List[str] = []
