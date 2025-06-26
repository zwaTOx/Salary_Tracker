from pydantic import BaseModel
from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List

from src.database import Sessionlocal
from src.service.token import get_current_user
router = APIRouter(
    prefix="/my/categories",
    tags=['Category']
)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/me')
async def get_salary(user: user_dependency, db: db_dependency):
    return {'status': 'OK'}