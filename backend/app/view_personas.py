from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemes import JWTBearer
from app.managers.db_manager import SessionLocal, Base
from sqlalchemy import select
from typing import List
from pydantic import BaseModel

# Modelo Pydantic para Persona
class PersonaIn(BaseModel):
    nombre: str
    apellido: str
    correo: str = None
    telefono: str = None
    nombre_contacto: str = None
    telefono_contacto: str = None
    tiene_whatsapp: bool = False
    direccion: str = None
    congregacion: str = None
    user_id: int = None
    nivel_actual: str = None

class PersonaOut(PersonaIn):
    id: int

router = APIRouter(prefix="/personas", tags=["personas"], dependencies=[Depends(JWTBearer())])

# SQLAlchemy modelo dinámico
from sqlalchemy import Table, MetaData
metadata = MetaData()
personas_table = Table('personas', metadata, autoload_with=SessionLocal().get_bind())

# Obtener todas las personas
@router.get('/', response_model=List[PersonaOut])
def get_personas():
    db = SessionLocal()
    result = db.execute(select(personas_table)).fetchall()
    db.close()
    # Convertir cada fila a diccionario usando el mapeo de columnas
    return [dict(row._mapping) for row in result]

# Crear persona
@router.post('/', response_model=PersonaOut)
def create_persona(persona: PersonaIn):
    db = SessionLocal()
    insert_stmt = personas_table.insert().values(**persona.dict())
    result = db.execute(insert_stmt)
    db.commit()
    persona_id = result.inserted_primary_key[0]
    db.close()
    return {"id": persona_id, **persona.dict()}

# Editar persona
@router.put('/{persona_id}', response_model=PersonaOut)
def update_persona(persona_id: int, persona: PersonaIn):
    db = SessionLocal()
    update_stmt = personas_table.update().where(personas_table.c.id == persona_id).values(**persona.dict())
    db.execute(update_stmt)
    db.commit()
    db.close()
    return {"id": persona_id, **persona.dict()}

# Eliminar persona
@router.delete('/{persona_id}')
def delete_persona(persona_id: int):
    db = SessionLocal()
    delete_stmt = personas_table.delete().where(personas_table.c.id == persona_id)
    db.execute(delete_stmt)
    db.commit()
    db.close()
    return {"message": "Persona eliminada"}
