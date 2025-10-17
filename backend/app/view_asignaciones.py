from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemes import JWTBearer
from app.managers.db_manager import SessionLocal, Base
from sqlalchemy import select
from typing import List
from pydantic import BaseModel

class AsignacionIn(BaseModel):
    user_id: int
    fecha_asignacion: str = None
    parte_asignacion: str = None
    creado_por: int = None
    numero_sala: int = None
    nota_adicional: str = None
    se_envio_asignacion: bool = False

class AsignacionOut(AsignacionIn):
    id: int
    fecha_creacion: str = None

router = APIRouter(prefix="/asignaciones", tags=["asignaciones"], dependencies=[Depends(JWTBearer())])

from sqlalchemy import Table, MetaData
metadata = MetaData()
asignaciones_table = Table('asignaciones', metadata, autoload_with=SessionLocal().get_bind())

@router.get('/', response_model=List[AsignacionOut])
def get_asignaciones():
    db = SessionLocal()
    result = db.execute(select(asignaciones_table)).fetchall()
    db.close()
    return [dict(row) for row in result]

@router.post('/', response_model=AsignacionOut)
def create_asignacion(asignacion: AsignacionIn):
    db = SessionLocal()
    insert_stmt = asignaciones_table.insert().values(**asignacion.dict())
    result = db.execute(insert_stmt)
    db.commit()
    asignacion_id = result.inserted_primary_key[0]
    db.close()
    return {"id": asignacion_id, **asignacion.dict()}

@router.put('/{asignacion_id}', response_model=AsignacionOut)
def update_asignacion(asignacion_id: int, asignacion: AsignacionIn):
    db = SessionLocal()
    update_stmt = asignaciones_table.update().where(asignaciones_table.c.id == asignacion_id).values(**asignacion.dict())
    db.execute(update_stmt)
    db.commit()
    db.close()
    return {"id": asignacion_id, **asignacion.dict()}

@router.delete('/{asignacion_id}')
def delete_asignacion(asignacion_id: int):
    db = SessionLocal()
    delete_stmt = asignaciones_table.delete().where(asignaciones_table.c.id == asignacion_id)
    db.execute(delete_stmt)
    db.commit()
    db.close()
    return {"message": "Asignación eliminada"}
