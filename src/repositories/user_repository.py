from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.models.user_model import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def check_user_exists(self, user_id):
        user = self.db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user
    