from typing import List, Literal
from sqlalchemy.orm import Session
from src.exceptions import ForbiddenException, NotFoundException, UnauthorizedException
from src.schemas.user_schemas import CreateUser, LoginUser, SalaryResponse, UserData, UpdateEmployeeInfo
from src.models.user_model import User
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def _get_user_by_email(self, email: str) -> User:
        user = self.db.query(User).filter(User.email == email).first()
        if user is None:
            raise NotFoundException("User not found")
        return user
    
    def _get_user_by_id(self, id: int) -> User:
        user = self.db.query(User).filter(User.id == id).first()
        if user is None:
            raise NotFoundException("User not found")
        return user

    def check_user_exists(self, user_email: str) -> bool:
        try:
            user = self._get_user_by_email(email=user_email)
        except NotFoundException:
            return False
        return True
    
    def check_admin_perms(self, user_id: int) -> bool:
        user = self._get_user_by_id(id=user_id)
        if not user.is_admin:
            raise ForbiddenException
        return True

    def create_user(self, user_data: CreateUser) -> int:
        user = User(
            email = user_data.email,
            hashed_password = bcrypt_context.hash(user_data.password)
        )
        self.db.add(user)
        self.db.commit()
        return user.id
    
    def login_user(self, user_data: LoginUser) -> UserData:
        user = self._get_user_by_email(user_data.email) 
        if not bcrypt_context.verify(user_data.password, user.hashed_password):
            raise UnauthorizedException('Invalid password')
        return UserData(
            id = user.id,
            email = user.email,
            username = user.username
        )
    
    def get_employee_info(self, user_id) -> SalaryResponse:
        user = self._get_user_by_id(user_id)
        return SalaryResponse(
            current_salary=user.current_salary,
            next_raise_date=user.next_raise_date
        )

    def get_all_employees(self, 
            offset: int = 0, 
            limit: int = 10, 
            sort_by: Literal['id', 'username', 'current_salary', 'email'] = 'id', 
            sort_order: Literal['asc', 'desc'] = 'asc') -> List[UserData]:
        if sort_order == 'asc':
            query = self.db.query(User).order_by(getattr(User, sort_by).asc())
        elif sort_order == 'desc':
            query = self.db.query(User).order_by(getattr(User, sort_by).desc())
        query = query.offset(offset).limit(limit)
        users = query.all()
        return [UserData(id=user.id, email=user.email, username=user.username) for user in users]

    def update_employee_info(self, user_id: int, info_to_update: UpdateEmployeeInfo) -> SalaryResponse:
        user = self._get_user_by_id(user_id)
        if info_to_update.current_salary is not None:
            user.current_salary = info_to_update.current_salary
        if info_to_update.next_raise_date is not None:
            user.next_raise_date = info_to_update.next_raise_date
        self.db.commit()
        return SalaryResponse(
            current_salary=user.current_salary,
            next_raise_date=user.next_raise_date
        )