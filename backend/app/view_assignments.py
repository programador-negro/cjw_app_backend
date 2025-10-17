from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemes import JWTBearer
from app.managers.db_manager import SessionLocal, Base
from sqlalchemy import select
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class AssignmentIn(BaseModel):
    user_id: int
    assignment_date: Optional[str] = None
    assignment_part: Optional[str] = None
    created_by: Optional[int] = None
    room_number: Optional[int] = None
    additional_notes: Optional[str] = None
    assignment_sent: bool = False

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class AssignmentOut(AssignmentIn):
    id: int
    created_at: Optional[str] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

router = APIRouter(prefix="/assignments", tags=["assignments"], dependencies=[Depends(JWTBearer())])

from sqlalchemy import Table, MetaData
metadata = MetaData()
assignments_table = Table('assignments', metadata, autoload_with=SessionLocal().get_bind())

@router.get('/', response_model=List[AssignmentOut])
def get_assignments():
    db = SessionLocal()
    result = db.execute(select(assignments_table)).fetchall()
    db.close()
    
    assignments_list = []
    for row in result:
        assignment_dict = dict(row._mapping)
        # Convert datetime objects to ISO format strings
        if assignment_dict.get('assignment_date'):
            assignment_dict['assignment_date'] = assignment_dict['assignment_date'].isoformat()
        if assignment_dict.get('created_at'):
            assignment_dict['created_at'] = assignment_dict['created_at'].isoformat()
        assignments_list.append(assignment_dict)
    
    return assignments_list

@router.post('/', response_model=AssignmentOut)
def create_assignment(assignment: AssignmentIn):
    db = SessionLocal()
    # Parse the assignment_date if it's provided
    assignment_data = assignment.dict()
    if assignment_data.get('assignment_date'):
        try:
            datetime.fromisoformat(assignment_data['assignment_date'])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    insert_stmt = assignments_table.insert().values(**assignment_data)
    result = db.execute(insert_stmt)
    db.commit()
    
    # Get the created record to include the created_at timestamp
    created_record = db.execute(
        select(assignments_table).where(assignments_table.c.id == result.inserted_primary_key[0])
    ).first()
    
    db.close()
    
    # Convert the record to dict and format dates
    record_dict = dict(created_record._mapping)
    if record_dict.get('assignment_date'):
        record_dict['assignment_date'] = record_dict['assignment_date'].isoformat()
    if record_dict.get('created_at'):
        record_dict['created_at'] = record_dict['created_at'].isoformat()
    
    return record_dict

@router.put('/{assignment_id}', response_model=AssignmentOut)
def update_assignment(assignment_id: int, assignment: AssignmentIn):
    db = SessionLocal()
    
    # Parse the assignment_date if it's provided
    assignment_data = assignment.dict()
    if assignment_data.get('assignment_date'):
        try:
            datetime.fromisoformat(assignment_data['assignment_date'])
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)")
    
    update_stmt = assignments_table.update().where(assignments_table.c.id == assignment_id).values(**assignment_data)
    db.execute(update_stmt)
    db.commit()
    
    # Get the updated record
    updated_record = db.execute(
        select(assignments_table).where(assignments_table.c.id == assignment_id)
    ).first()
    
    if not updated_record:
        db.close()
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    db.close()
    
    # Convert the record to dict and format dates
    record_dict = dict(updated_record._mapping)
    if record_dict.get('assignment_date'):
        record_dict['assignment_date'] = record_dict['assignment_date'].isoformat()
    if record_dict.get('created_at'):
        record_dict['created_at'] = record_dict['created_at'].isoformat()
    
    return record_dict

@router.delete('/{assignment_id}')
def delete_assignment(assignment_id: int):
    db = SessionLocal()
    delete_stmt = assignments_table.delete().where(assignments_table.c.id == assignment_id)
    db.execute(delete_stmt)
    db.commit()
    db.close()
    return {"message": "Assignment deleted"}