from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemes import JWTBearer
from app.managers.db_manager import SessionLocal, Base
from sqlalchemy import select
from typing import List
from pydantic import BaseModel

class PrivilegioIn(BaseModel):
    user_id: int
    fecha_privilegio: str = None
    parte_privilegio: str = None
    creado_por: int = None
    numero_sala: int = None
    nota_adicional: str = None
    se_envio_privilegio: bool = False

class PrivilegioOut(PrivilegioIn):
    id: int
    fecha_creacion: str = None

router = APIRouter(prefix="/privilegios", tags=["privilegios"], dependencies=[Depends(JWTBearer())])

from sqlalchemy import Table, MetaData
metadata = MetaData()
privilegios_table = Table('privilegios', metadata, autoload_with=SessionLocal().get_bind())

@router.get('/', response_model=List[PrivilegioOut])
def get_privilegios():
    db = SessionLocal()
    result = db.execute(select(privilegios_table)).fetchall()
    db.close()
    return [dict(row) for row in result]

@router.post('/', response_model=PrivilegioOut)
def create_privilegio(privilegio: PrivilegioIn):
    db = SessionLocal()
    insert_stmt = privilegios_table.insert().values(**privilegio.dict())
    result = db.execute(insert_stmt)
    db.commit()
    privilegio_id = result.inserted_primary_key[0]
    db.close()
    return {"id": privilegio_id, **privilegio.dict()}

@router.put('/{privilegio_id}', response_model=PrivilegioOut)
def update_privilegio(privilegio_id: int, privilegio: PrivilegioIn):
    db = SessionLocal()
    update_stmt = privilegios_table.update().where(privilegios_table.c.id == privilegio_id).values(**privilegio.dict())
    db.execute(update_stmt)
    db.commit()
    db.close()
    return {"id": privilegio_id, **privilegio.dict()}

@router.delete('/{privilegio_id}')
def delete_privilegio(privilegio_id: int):
    db = SessionLocal()
    delete_stmt = privilegios_table.delete().where(privilegios_table.c.id == privilegio_id)
    db.execute(delete_stmt)
    db.commit()
    db.close()
    return {"message": "Privilegio eliminado"}
