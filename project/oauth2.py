from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi import Depends, status, HTTPException

from . import database
from project.config import settings

import base64

from typing import List
from project.jwt_auth import AuthJWT
from pydantic import BaseModel

from project.crud import get_user_by_id

class Settings(BaseModel):
    authjwt_algorithm: str = settings.jwt_algorithm
    authjwt_decode_algorithms: List[str] = [settings.jwt_algorithm]
    authjwt_token_location: str = "cookies"
    authjwt_access_cookie_key: str = 'access_token'
    authjwt_refresh_cookie_key: str = 'refresh_token'
    authjwt_cookie_secure: bool = False
    authjwt_cookie_csrf_protect: bool = False
    authjwt_public_key: str = base64.b64decode(
        settings.jwt_public_key).decode('utf-8')
    authjwt_private_key: str = base64.b64decode(
        settings.jwt_private_key).decode('utf-8')
    
@AuthJWT.load_config
def get_config():
    return Settings()

class UserIsNotAdmin(Exception):
    pass

async def require_user(db: Session = Depends(database.get_db_session), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = await get_user_by_id(db, user_id)
        if not user:
            credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Could not validate credentials", 
            headers={"WWW-Authenticate": "Bearer"}
            )
            raise credentials_exception
    
    except Exception as e:

        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return user


async def require_admin(db: Session = Depends(database.get_db_session), Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
        user_id = Authorize.get_jwt_subject()
        user = await get_user_by_id(db, user_id)
        if not user:
            credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Could not validate credentials", 
            headers={"WWW-Authenticate": "Bearer"}
            )
            raise credentials_exception
        if not user.is_admin:
            raise UserIsNotAdmin("You are not admin")
    
    except Exception as e:
        error = e.__class__.__name__
        print(error)
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not logged in')
        if error == "UserIsNotAdmin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not admin')
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Token is invalid or has expired')
    return user