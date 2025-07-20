from fastapi import APIRouter, FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, List
from src.schemas.user_schemas import SalaryResponse
from src.service.user_service import UserService

from src.database import get_db
from src.service.token import get_current_user
router = APIRouter(
    prefix="/users",
    tags=['Profile']
)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/me",
    status_code=status.HTTP_200_OK,
    response_model=SalaryResponse,
    description="Get current user's employee info",
    summary="Get Employee Info",
    responses={
        status.HTTP_200_OK: {
            "description": "Employee info retrieved successfully"},
    })
async def get_employee_info(user: user_dependency, db: db_dependency):
    info = UserService(db).get_employee_info(user['id'])
    return info
