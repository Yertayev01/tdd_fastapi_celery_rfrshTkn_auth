from contextlib import asynccontextmanager
from broadcaster import Broadcast
from fastapi import FastAPI

from project.config import settings

broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    from project.logging import configure_logging          # new
    configure_logging()                                    # new

    from project.celery_utils import create_celery
    app.celery_app = create_celery()

    from project.users import users_router
    app.include_router(users_router)

    from project.tdd import tdd_router                   # new
    app.include_router(tdd_router)                       # new

    from project.ws import ws_router                   # new
    app.include_router(ws_router)                      # new

    from project.ws.views import register_socketio_app         # new
    register_socketio_app(app)                                 # new
    
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app