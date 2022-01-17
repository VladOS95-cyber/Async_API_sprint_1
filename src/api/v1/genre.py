from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from models.genre import ResponceGenreDetailed
from services.genre import GenreService, get_genre_service
from services.utils import get_params

router = APIRouter()


@router.get(
    "/search",
    response_model=list[ResponceGenreDetailed],
    summary="List of suitable genre",
    description="List of genre with sort, filter and pagination and text search",
    response_description="List of genres with id",
)
@router.get(
    "",
    response_model=list[ResponceGenreDetailed],
    summary="List of genre",
    description="List of genre with sort, filter and pagination",
    response_description="List of genres with id",
)
async def genres_list(
    request: Request, genre_service: GenreService = Depends(get_genre_service)
) -> list[ResponceGenreDetailed]:
    params = get_params(request)
    genres = await genre_service.get_by_params(**params)
    if not genres:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="GENRE_NOT_FOUND")
    return [
        ResponceGenreDetailed(
            id=genre.id,
            name=genre.name,
            description=genre.description,
            films=genre.films,
        )
        for genre in genres
    ]


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
