from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.film import FilmService, get_film_service
from models.film import ResponceFilm, ResponceFilms

router = APIRouter()



@router.get("/all", response_model=ResponceFilms)
async def films(film_service: FilmService = Depends(get_film_service)) -> ResponceFilms:
    films = await film_service.get_all_films()
    return films


@router.get("/{film_id}", response_model=ResponceFilm)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> ResponceFilm:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return ResponceFilm(
        id=film.id,
        imdb_rating=film.imdb_rating,
        genre=film.genre,
        title=film.title,
        description=film.description,
        director=film.director,
        actors_names=film.actors_names,
        writers_names=film.writers_names,
    )
