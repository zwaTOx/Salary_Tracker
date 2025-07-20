from typing import Literal
from sqlalchemy.orm import Session

from src.service.token import create_access_token
from src.exceptions import ForbiddenException, BadRequestException
from src.repositories.user_repository import UserRepository
from src.schemas.user_schemas import CreateUser, LoginUser, SalaryResponse, UpdateEmployeeInfo

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

    def update_employee_info(self, admin_id: int, user_id: int, info_to_update: UpdateEmployeeInfo) -> SalaryResponse:
        UserRepository(self.db).check_admin_perms(user_id=admin_id)
        if user_id == admin_id:
            raise ForbiddenException
        updated_info = UserRepository(self.db).update_employee_info(user_id=user_id, info_to_update=info_to_update)
        return updated_info

    def get_all_employees(self, 
        admin_id: int,
        offset: int = 0, 
        limit: int = 10, 
        sort_by: Literal['id', 'username', 'current_salary', 'email'] = 'id', 
        sort_order: Literal['asc', 'desc'] = 'asc'
    ) -> list[SalaryResponse]:
        UserRepository(self.db).check_admin_perms(user_id=admin_id)
        return UserRepository(self.db).get_all_employees(
            offset=offset,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order
        )