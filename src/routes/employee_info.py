from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from src.service.user_service import UserService

from src.database import Sessionlocal
from src.service.token import get_current_user
router = APIRouter(
    prefix="/me",
    tags=['Profile']
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("")
async def get_employee_info(user: user_dependency, db: db_dependency):
    info = UserService(db).get_employee_info(user['id'])
    return info