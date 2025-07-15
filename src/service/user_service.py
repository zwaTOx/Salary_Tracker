from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.service.token import create_access_token
from src.exceptions import NotFoundException, BadRequestException
from src.repositories.user_repository import UserRepository
from src.schemas.user_schemas import CreateUser, LoginUser

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: CreateUser) -> int:
        if UserRepository(self.db).check_user_exists(user_data.email):
            raise BadRequestException('User is already exists')
        user_id = UserRepository(self.db).create_user(user_data) 
        return user_id
    
    def auth_user(self, user_login_rq: LoginUser):
        user_data = UserRepository(self.db).login_user(user_login_rq)
        token = create_access_token(id=user_data.id, email=user_data.email)
        return token
    
    def get_employee_info(self, user_id):
        return UserRepository(self.db).get_employee_info(user_id)