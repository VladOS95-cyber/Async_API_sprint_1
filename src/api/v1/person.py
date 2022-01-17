from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Request

from models.person import ReponcePersonDetailed
from services.person import PersonService, get_person_service
from services.utils import get_params

router = APIRouter()


@router.get(
    "/search",
    response_model=list[ReponcePersonDetailed],
    summary="List of suitable person",
    description="List of persons with full_name, roles and film_ids",
    response_description="List of persons with id",
)
@router.get(
    "",
    response_model=list[ReponcePersonDetailed],
    summary="List of person",
    description="List of persons with full_name, roles and film_ids",
    response_description="List of persons with id",
)
async def persons_list(
    request: Request, person_service: PersonService = Depends(get_person_service)
) -> list[ReponcePersonDetailed]:
    params = get_params(request)
    person_list = await person_service.get_by_params(**params)
    if not person_list:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="PERSON_NOT_FOUND")
    return [
        ReponcePersonDetailed(
            id=person.id,
            full_name=person.full_name,
            roles=person.roles,
            films=person.films,
        )
        for person in person_list
    ]


@router.get("/{person_id}", response_model=ReponcePersonDetailed)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> ReponcePersonDetailed:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return ReponcePersonDetailed(
        id=person.id,
        full_name=person.full_name,
        roles=person.roles,
        films=person.films,
    )
