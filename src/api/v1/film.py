from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service

router = APIRouter()


class Film(BaseModel):
    id: str
    imdb_rating: Union[float, None] = 0.0
    genre: List[str] = []
    title: str
    description: Union[str, None] = ""
    director: Union[str, None] = ""
    actors_names: List[str] = []
    writers_names: List[str] = []


class Films(BaseModel):
    films: List[Film] = []


@router.get("/all", response_model=Films)
async def films(film_service: FilmService = Depends(get_film_service)) -> Films:
    films = await film_service.get_all_films()
    return films


@router.get("/{film_id}", response_model=Film)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return Film(
        id=film.id,
        imdb_rating=film.imdb_rating,
        genre=film.genre,
        title=film.title,
        description=film.description,
        director=film.director,
        actors_names=film.actors_names,
        writers_names=film.writers_names,
    )
