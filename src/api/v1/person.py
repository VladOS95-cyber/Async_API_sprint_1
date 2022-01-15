from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from models.person import ReponcePersonDetailed, ResponcePersons

from services.person import PersonService, get_person_service

router = APIRouter()


@router.get("/all", response_model=ResponcePersons)
async def person(
    person_service: PersonService = Depends(get_person_service),
) -> ResponcePersons:
    persons = await person_service.get_all_persons()
    return persons


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
