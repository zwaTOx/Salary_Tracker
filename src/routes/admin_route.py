from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from src.schemas.user_schemas import SalaryResponse, UpdateEmployeeInfo
from src.service.user_service import UserService

from src.database import get_db
from src.service.token import get_current_user
from typing import Literal

router = APIRouter(
    prefix="/users",
    tags=['Admin']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/')
def get_employees(
    user: user_dependency,
    db: db_dependency,
    offset: int = 0,
    limit: int = 10,
    sort_by: Literal['id', 'username', 'current_salary'] = 'id',
    sort_order: Literal['asc', 'desc'] = 'asc'  
):  
    employees = UserService(db).get_all_employees(offset=offset, limit=limit, sort_by=sort_by, sort_order=sort_order)
    return employees


@router.put("/{user_id}",
    status_code=200,
    response_model=SalaryResponse)
def update_employee_info(
    user_id: int,
    info_to_update: UpdateEmployeeInfo, 
    user: user_dependency, 
    db: db_dependency
):
    updated_info = UserService(db).update_employee_info(admin_id=user['id'], user_id=user_id, info_to_update=info_to_update)
    return updated_info