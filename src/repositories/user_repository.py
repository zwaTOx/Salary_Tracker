from sqlalchemy.orm import Session
from src.exceptions import NotFoundException
from src.schemas.user_schemas import CreateUser, UserData
from src.models.user_model import User
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user(self, email: str):
        user = self.db.query(User).filter(User.email == email).first()
        if user is None:
            raise NotFoundException("User not found")
        return UserData(
            id=user.id,
            email=user.email,
            username=user.username
            )
    
    def create_user(self, user_data: CreateUser) -> int:
        user = User(
            email = user_data.email,
            hashed_password = bcrypt_context.hash(user_data.password)
        )
        self.db.add(user)
        self.db.commit()
        return user.id