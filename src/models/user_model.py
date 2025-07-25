from datetime import datetime, timezone
from sqlalchemy import (
    Column,DateTime, 
    Integer, String, Boolean
    )
from src.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), default='user')
    email = Column(String(100), unique=True)
    hashed_password = Column(String(256))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    current_salary = Column(Integer, nullable=True) 
    next_raise_date = Column(DateTime, nullable=True) 
    is_admin = Column(Boolean, default=False)  # False - employee, True - admin