from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from project import  utils
from project.users import models, schemas
from sqlalchemy import func
import math
from sqlalchemy import and_
import re
#from app.core.utils import hash_password

#user
async def get_user_by_id(db: Session, user_id: str) -> models.User:
    return db.query(models.User).filter(models.User.USER_ID == user_id).first()

async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.USER_NM == username).first()

async def get_users(db: Session) -> List[models.User]:
    return db.query(models.User).all()

async def get_user_by_username(db: Session, username: str) -> models.User:
    return db.query(models.User).filter(models.User.USER_NM == username).first()

async def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.EMAIL == email).first()

async def user_create(db: Session, user: schemas.UserCreate) -> models.User:
    # Check if email exists
    existing_email = await get_user_by_email(db, user.EMAIL)
    if existing_email:
        raise HTTPException(detail=f"Email {user.EMAIL} is already registered", status_code=status.HTTP_409_CONFLICT)

    # Check if username exists
    existing_username = await get_user_by_username(db, user.USER_NM)
    if existing_username:
        raise HTTPException(detail=f"Username {user.USER_NM} is already taken", status_code=status.HTTP_409_CONFLICT)
    
    user.PSSWRD = await utils.hash_password(user.PSSWRD)
    db_user = models.User(
        **user.dict(),
    )

    user.REG_USER_ID = user.USER_ID
    user.MOD_USER_ID = user.USER_ID

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def user_update(db: Session, user_id: int, user: schemas.UserUpdate) -> models.User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = await utils.hash_password(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def user_delete(db: Session, user_id: int) -> models.User:
    db_user = await get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

#photo
async def photo_create(db: Session, photo: schemas.PhotoCreate):
    photo = models.Photo(
        **photo.dict()
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

