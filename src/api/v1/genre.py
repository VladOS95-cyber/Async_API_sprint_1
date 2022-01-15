from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService, get_genre_service
from models.genre import ResponceGenreDetailed, ResponceGenres

router = APIRouter()


@router.get("/all", response_model=ResponceGenres)
async def genre(genre_service: GenreService = Depends(get_genre_service)) -> ResponceGenres:
    Genres = await genre_service.get_all_genres()
    return Genres


@router.get("/{genre_id}", response_model=ResponceGenreDetailed)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> ResponceGenreDetailed:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return ResponceGenreDetailed(
        id=genre.id,
        name=genre.name,
        description=genre.description,
        films=genre.films,
    )
