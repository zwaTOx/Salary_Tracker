from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.exceptions import NotFoundException, BadRequestException
from src.repositories.user_repository import UserRepository
from src.schemas.user_schemas import CreateUser


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: CreateUser) -> int:
        try:
            founded_user = UserRepository(self.db).get_user(user_data.email)
            raise BadRequestException(
                detail='User is already exists'
            )
        except NotFoundException:
            user_id = UserRepository(self.db).create_user(user_data)
        return user_id