
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.database import get_db
from src.service.user_service import UserService
from src.schemas.user_schemas import CreateUser, LoginUser
from src.schemas.token_schemas import Token

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

router = APIRouter(
    tags=['Auth']
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/registration", 
    status_code=status.HTTP_201_CREATED,
    description="Register a new user",
    summary="User Registration",
    responses={
        status.HTTP_201_CREATED: {
            "description": "User created successfully"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "User is already exists"}
    }) 
async def register_user(
    create_user_rq: CreateUser,
    db: db_dependency
    ):
    user_id = UserService(db).create_user(user_data=create_user_rq)
    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={"Location": f"/users/{user_id}"}  
    )

@router.post('/auth',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    description="Authenticate user and return access token",
    summary="User Authentication",
    responses={
        status.HTTP_200_OK: {
            'description': 'User auth successfully'},
        status.HTTP_404_NOT_FOUND: {
            'description': 'User with this email not found'},
        status.HTTP_401_UNAUTHORIZED: {
            'description': 'Invalid password'}
    })
async def auth_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    token = UserService(db).auth_user(
        LoginUser(
            email=form_data.username, 
            password=form_data.password)
        )
    return Token(access_token=token, token_type='bearer')