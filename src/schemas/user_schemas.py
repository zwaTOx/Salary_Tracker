from datetime import datetime
import re
from typing import Optional
from pydantic import BaseModel, field_validator

EMAIL_MASK = r'^[A-Za-z0-9\-_.]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-.]{2,}$'
PASSWORD_MASK = r'^[A-Za-z0-9!#$%&*+\-<=>?@^_]{8,16}$'

def validate_email(value: str) -> str:
    if not re.match(EMAIL_MASK, value):
        raise ValueError('Invalid login format')
    return value

def validate_password(value: str) -> str:
    if not re.match(PASSWORD_MASK, value):
        raise ValueError('Invalid password format')
    return value

class _UserAuthBase(BaseModel):
    email: str
    password: str
    
    # @field_validator('email')
    # def validate_email_field(cls, value):
    #     return validate_email(value)
    
    # @field_validator('password')
    # def validate_password_field(cls, value):
    #     return validate_password(value)

class CreateUser(_UserAuthBase):
    pass

class LoginUser(_UserAuthBase):
    pass

class UserData(BaseModel):
    id: int
    email: str
    username: str 

class SalaryResponse(BaseModel):
    current_salary: int
    next_raise_date: Optional[datetime]

