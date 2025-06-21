
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.database import Sessionlocal
from src.service.user import UserService
from src.schemas.user_schemas import CreateUser

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

router = APIRouter(
    tags=['Auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='login')
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/registration", 
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
        400: {"description": "User is already exists"}
    }
    ) 
async def register_user(
    create_user_rq: CreateUser,
    db: db_dependency
    ):
    user_id = UserService(db).create_user(user_data=create_user_rq)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/users/{user_id}"}  
    )
