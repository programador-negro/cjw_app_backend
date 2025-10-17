from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemes import JWTBearer
from app.managers.db_manager import SessionLocal, Base
from sqlalchemy import select
from typing import List
from pydantic import BaseModel

# Pydantic model for Person
class PersonIn(BaseModel):
    first_name: str
    last_name: str
    email: str = None
    phone: str = None
    contact_name: str = None
    contact_phone: str = None
    has_whatsapp: bool = False
    address: str = None
    congregation: str = None
    user_id: int = None
    current_level: str = None

class PersonOut(PersonIn):
    id: int

router = APIRouter(prefix="/people", tags=["people"], dependencies=[Depends(JWTBearer())])

# SQLAlchemy dynamic model
from sqlalchemy import Table, MetaData
metadata = MetaData()
people_table = Table('people', metadata, autoload_with=SessionLocal().get_bind())

# Get all people
@router.get('/', response_model=List[PersonOut])
def get_people():
    db = SessionLocal()
    result = db.execute(select(people_table)).fetchall()
    db.close()
    # Convert each row to dictionary using SQLAlchemy row mapping
    return [dict(row._mapping) for row in result]

# Create person
@router.post('/', response_model=PersonOut)
def create_person(person: PersonIn):
    db = SessionLocal()
    insert_stmt = people_table.insert().values(**person.dict())
    result = db.execute(insert_stmt)
    db.commit()
    person_id = result.inserted_primary_key[0]
    db.close()
    return {"id": person_id, **person.dict()}

# Edit person
@router.put('/{person_id}', response_model=PersonOut)
def update_person(person_id: int, person: PersonIn):
    db = SessionLocal()
    update_stmt = people_table.update().where(people_table.c.id == person_id).values(**person.dict())
    db.execute(update_stmt)
    db.commit()
    db.close()
    return {"id": person_id, **person.dict()}

# Delete person
@router.delete('/{person_id}')
def delete_person(person_id: int):
    db = SessionLocal()
    delete_stmt = people_table.delete().where(people_table.c.id == person_id)
    db.execute(delete_stmt)
    db.commit()
    db.close()
    return {"message": "Person deleted"}