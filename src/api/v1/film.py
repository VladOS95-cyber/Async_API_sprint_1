from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from models.film import FilmShortResponse, ResponceFilm
from services.film import FilmService, get_film_service
from services.utils import get_params

router = APIRouter()


@router.get(
    "/search",
    response_model=list[FilmShortResponse],
    summary="List of suitable films",
    description="List of films with title and imdb_rating, with sort, filter and pagination and text search",
    response_description="List of films with id",
)
@router.get(
    '',
    response_model=list[FilmShortResponse],
    summary="List of films",
    description="List of films with title and imdb_rating, with sort, filter and pagination",
    response_description="List of films with id",
)
async def films_list(
    request: Request, film_service: FilmService = Depends(get_film_service)
) -> list[FilmShortResponse]:
    params = get_params(request)
    film_list = await film_service.get_by_params(**params)
    if not film_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="FILM_NOT_FOUND")
    return [
        FilmShortResponse(
            id=film.id,
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in film_list
    ]


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
