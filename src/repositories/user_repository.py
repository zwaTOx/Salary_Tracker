from sqlalchemy.orm import Session
from src.exceptions import NotFoundException, UnauthorizedException
from src.schemas.user_schemas import CreateUser, LoginUser, UserData
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
    
    def check_user_exists(self, user_email) -> bool:
        try:
            user = self._get_user_by_email(email=user_email)
        except NotFoundException:
            return False
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