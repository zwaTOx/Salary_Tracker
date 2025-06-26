from datetime import datetime, timedelta
import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth')

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def create_access_token(id: str, email: str, minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES):
        payload = {'id': id, 'email': email}
        expires = datetime.now() + timedelta(minutes=minutes)
        payload.update({'exp': expires})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        email: str = payload.get('email')
        user_id: int = payload.get('id')
        if email is None or user_id is None:
            raise HTTPException(status_code=401, detail='Could not validate user.')
        return {'email': email, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not validate user.')