import logging
import random
from string import ascii_lowercase

import requests
from celery.result import AsyncResult
from fastapi import Request, Depends
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import users_router
from project.users.schemas import UserBody
from project.users.tasks import sample_task, task_process_notification, task_send_welcome_email, task_add_subscribe
from project.users.models import User
from project.database import get_db_session

#anchor world imports

from fastapi import status, HTTPException, Response
from project import crud, database
from project.users import schemas
import typing as t
from sqlalchemy.orm import Session
from project.oauth2 import AuthJWT
from datetime import datetime, timedelta
from project.config import settings

from project import utils, oauth2
from . import models


logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="project/users/templates")


def api_call(email: str):
    # used for testing a failed api call
    if random.choice([0, 1]):
        raise Exception("random processing error")

    # used for simulating a call to a third-party api
    requests.post("https://httpbin.org/delay/5")


@users_router.get("/form/")
def form_example_get(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@users_router.post("/form/")
def form_example_post(user_body: UserBody):
    task = sample_task.delay(user_body.email)
    return JSONResponse({"task_id": task.task_id})


@users_router.get("/task_status/")
def task_status(task_id: str):
    task = AsyncResult(task_id)
    state = task.state

    if state == 'FAILURE':
        error = str(task.result)
        response = {
            'state': state,
            'error': error,
        }
    else:
        response = {
            'state': state,
        }
    return JSONResponse(response)


@users_router.post("/webhook_test/")
def webhook_test():
    if not random.choice([0, 1]):
        # mimic an error
        raise Exception()

    # blocking process
    requests.post("https://httpbin.org/delay/5")
    return "pong"


@users_router.post("/webhook_test_async/")
def webhook_test_async():
    task = task_process_notification.delay()
    print(task.id)
    return "pong"

@users_router.get("/form_ws/")
def form_ws_example(request: Request):
    return templates.TemplateResponse("form_ws.html", {"request": request})

@users_router.get("/form_socketio/")
def form_socketio_example(request: Request):
    return templates.TemplateResponse("form_socketio.html", {"request": request})


def random_username():
    username = "".join([random.choice(ascii_lowercase) for i in range(5)])
    return username

@users_router.get("/transaction_celery/")
def transaction_celery(session: Session = Depends(get_db_session)):
    username = random_username()
    user = User(
        username=f'{username}',
        email=f'{username}@test.com',
    )
    with session.begin():
        session.add(user)

    logger.info(f"user {user.id} {user.username} is persistent now")       # new
    task_send_welcome_email.delay(user.id)
    return {"message": "done"}

@users_router.post("/user_subscribe/")
def user_subscribe(
    user_body: UserBody,
    session: Session = Depends(get_db_session)
):
    with session.begin():
        user = session.query(User).filter_by(
            username=user_body.username
        ).first()
        if not user:
            user = User(
                username=user_body.username,
                email=user_body.email,
            )
            session.add(user)
    task_add_subscribe.delay(user.id)
    return {"message": "send task to Celery successfully"}

#anchor world user endpoints
# ACCESS_TOKEN_EXPIRES_IN = settings.access_token_expires_in
# REFRESH_TOKEN_EXPIRES_IN = settings.refresh_token_expires_in

ACCESS_TOKEN_EXPIRES_IN = 1440
REFRESH_TOKEN_EXPIRES_IN = 86400





@users_router.post("/register", response_model=schemas.UserReturn, status_code=status.HTTP_201_CREATED)
async def register(
                    user: schemas.UserCreate,
                    #photo: UploadFile,
                    db: Session = Depends(database.get_db_session)
                   ):
    
    # path = await utils.save_photo(photo)
    # await crud.photo_create(db, schemas.PhotoCreate(user_id=user.user_id, photo_url=path))
    
    user = await crud.user_create(db, user)
    return user


@users_router.post('/login')
async def login(payload: schemas.UserLogin, 
                response: Response, Authorize: AuthJWT = Depends(), 
                db: Session = Depends(database.get_db_session)):
    # Check if the user exist
    user = db.query(models.User).filter(
        models.User.EMAIL == payload.EMAIL).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User does not exist')

    # Check if the password is valid
    if not await utils.verify_password(payload.PSSWRD, user.PSSWRD):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Incorrect Email or Password')
    # Create access token
    access_token = Authorize.create_access_token(
        subject=str(user.USER_ID), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))
    # Create refresh token
    refresh_token = Authorize.create_refresh_token(
        subject=str(user.USER_ID), expires_time=timedelta(minutes=REFRESH_TOKEN_EXPIRES_IN))

    # Store refresh and access tokens in cookie
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('refresh_token', refresh_token, REFRESH_TOKEN_EXPIRES_IN * 60,
                        REFRESH_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    # Send both access
    return {'access_token': access_token}


@users_router.get('/me', status_code=status.HTTP_200_OK, response_model=schemas.UserReturn)
async def me(current_user: models.User = Depends(oauth2.require_user)):
    return current_user


@users_router.get('/refresh')
async def refresh_token(response: Response, 
                        Authorize: AuthJWT = Depends(), 
                        db: Session = Depends(database.get_db_session)):
    try:
        Authorize.jwt_refresh_token_required()

        user_id = Authorize.get_jwt_subject()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not refresh access token')
        user = await crud.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='The user belonging to this token no logger exist')
        access_token = Authorize.create_access_token(
            subject=str(user.USER_ID), expires_time=timedelta(minutes=ACCESS_TOKEN_EXPIRES_IN))

    except Exception as e:
        error = e.__class__.__name__
        if error == 'MissingTokenError':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    response.set_cookie('access_token', access_token, ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
    response.set_cookie('logged_in', 'True', ACCESS_TOKEN_EXPIRES_IN * 60,
                        ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
    return {'access_token': access_token}


@users_router.get('/logout', status_code=status.HTTP_200_OK)
async def logout(response: Response, Authorize: AuthJWT = Depends()):
    Authorize.unset_jwt_cookies()
    response.set_cookie('logged_in', '', -1)
    return {'status': 'success'}
