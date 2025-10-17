from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemes import JWTBearer
from app.managers.db_manager import SessionLocal, Base
from sqlalchemy import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class PrivilegeIn(BaseModel):
    user_id: int
    privilege_date: Optional[str] = None
    privilege_part: Optional[str] = None
    created_by: Optional[int] = None
    room_number: Optional[int] = None
    additional_notes: Optional[str] = None
    privilege_sent: bool = False

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class PrivilegeOut(PrivilegeIn):
    id: int
    created_at: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

router = APIRouter(prefix="/privileges", tags=["privileges"], dependencies=[Depends(JWTBearer())])

from sqlalchemy import Table, MetaData
metadata = MetaData()
privileges_table = Table('privileges', metadata, autoload_with=SessionLocal().get_bind())

@router.get('/', response_model=List[PrivilegeOut])
def get_privileges():
    db = SessionLocal()
    result = db.execute(select(privileges_table)).fetchall()
    db.close()
    
    privileges_list = []
    for row in result:
        privilege_dict = dict(row._mapping)
        # Convert datetime objects to ISO format strings
        if privilege_dict.get('privilege_date'):
            privilege_dict['privilege_date'] = privilege_dict['privilege_date'].isoformat()
        if privilege_dict.get('created_at'):
            privilege_dict['created_at'] = privilege_dict['created_at'].isoformat()
        privileges_list.append(privilege_dict)
    
    return privileges_list

@router.post('/', response_model=PrivilegeOut)
def create_privilege(privilege: PrivilegeIn):
    db = SessionLocal()
    # Parse the privilege_date if it's provided
    privilege_data = privilege.dict()
    if privilege_data.get('privilege_date'):
        try:
            datetime.fromisoformat(privilege_data['privilege_date'])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    insert_stmt = privileges_table.insert().values(**privilege_data)
    result = db.execute(insert_stmt)
    db.commit()
    
    # Get the created record to include the created_at timestamp
    created_record = db.execute(
        select(privileges_table).where(privileges_table.c.id == result.inserted_primary_key[0])
    ).first()
    
    db.close()
    
    # Convert the record to dict and format dates
    record_dict = dict(created_record._mapping)
    if record_dict.get('privilege_date'):
        record_dict['privilege_date'] = record_dict['privilege_date'].isoformat()
    if record_dict.get('created_at'):
        record_dict['created_at'] = record_dict['created_at'].isoformat()
    
    return record_dict

@router.put('/{privilege_id}', response_model=PrivilegeOut)
def update_privilege(privilege_id: int, privilege: PrivilegeIn):
    db = SessionLocal()
    
    # Parse the privilege_date if it's provided
    privilege_data = privilege.dict()
    if privilege_data.get('privilege_date'):
        try:
            datetime.fromisoformat(privilege_data['privilege_date'])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    update_stmt = privileges_table.update().where(privileges_table.c.id == privilege_id).values(**privilege_data)
    db.execute(update_stmt)
    db.commit()
    
    # Get the updated record
    updated_record = db.execute(
        select(privileges_table).where(privileges_table.c.id == privilege_id)
    ).first()
    
    if not updated_record:
        db.close()
        raise HTTPException(status_code=404, detail="Privilege not found")
    
    db.close()
    
    # Convert the record to dict and format dates
    record_dict = dict(updated_record._mapping)
    if record_dict.get('privilege_date'):
        record_dict['privilege_date'] = record_dict['privilege_date'].isoformat()
    if record_dict.get('created_at'):
        record_dict['created_at'] = record_dict['created_at'].isoformat()
    
    return record_dict

@router.delete('/{privilege_id}')
def delete_privilege(privilege_id: int):
    db = SessionLocal()
    delete_stmt = privileges_table.delete().where(privileges_table.c.id == privilege_id)
    db.execute(delete_stmt)
    db.commit()
    db.close()
    return {"message": "Privilege deleted"}