from http import HTTPStatus
from typing import List, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.v1.person import InfoFilm
from services.genre import GenreService, get_genre_service

router = APIRouter()


class GenreDetailed(BaseModel):
    id: str
    name: str
    description: Union[str, None] = ""
    films: List[InfoFilm] = []


class Genres(BaseModel):
    genres: List[GenreDetailed] = []


@router.get("/all", response_model=Genres)
async def genre(genre_service: GenreService = Depends(get_genre_service)) -> Genres:
    Genres = await genre_service.get_all_genres()
    return Genres


@router.get("/{genre_id}", response_model=GenreDetailed)
async def genre_details(
    genre_id: str, genre_service: GenreService = Depends(get_genre_service)
) -> GenreDetailed:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    return GenreDetailed(
        id=genre.id,
        name=genre.name,
        description=genre.description,
        films=genre.films,
    )
