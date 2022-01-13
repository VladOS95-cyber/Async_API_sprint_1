from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from services.person import PersonService, get_person_service

router = APIRouter()


class InfoFilm(BaseModel):
    id: str
    title: str


class PersonDetailed(BaseModel):
    id: str
    full_name: str
    roles: List[str] = []
    films: List[InfoFilm] = []


class Persons(BaseModel):
    persons: List[PersonDetailed] = []


@router.get("/all", response_model=Persons)
async def person(
    person_service: PersonService = Depends(get_person_service),
) -> Persons:
    persons = await person_service.get_all_persons()
    return persons


@router.get("/{person_id}", response_model=PersonDetailed)
async def person_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> PersonDetailed:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return PersonDetailed(
        id=person.id,
        full_name=person.full_name,
        roles=person.roles,
        films=person.films,
    )
