"""Main module imported in the project.

Here you include the routers for the application and middleware used.
"""
import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from controllers.users_controllers import user_router
from controllers.base_controllers import base_router
from controllers.atom_controllers import atom_router
from controllers.api_controllers import api_router
from controllers.task_controllers import task_router
from controllers.ws_controllers import ws_router
from controllers.utils_controllers import utils_router
from controllers.redis_controllers import redis_router
from data import (
    async_session,
    User,
    create_database_app,
    create_mongodb_schemas,
)
from config import config
from cache import initialize_cache
from logger import initialize_logger
from utils import get_password_hash
from middleware import TimeRequestMiddleware

middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
    ),
    Middleware(TimeRequestMiddleware),
]


app = FastAPI(middleware=middleware)


app.mount("/static", StaticFiles(directory="static"), name="static")

# include routes
app.include_router(user_router)
app.include_router(atom_router)
app.include_router(base_router)
app.include_router(api_router)
app.include_router(task_router)
app.include_router(ws_router)
app.include_router(utils_router)
app.include_router(redis_router)


@app.on_event("startup")
async def user_on_startup(session: AsyncSession = async_session()):
    """Creates a user at startup.

    Args:
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).
    """

    initialize_cache()
    initialize_logger()
    create_database_app()
    create_mongodb_schemas()

    if config.user_name and config.user_email and config.user_password:
        params = {
            "username": config.user_name,
            "email": config.user_email,
        }

        try:
            hashed_pass = get_password_hash(config.user_password)
            params["hashed_pass"] = hashed_pass
            await User.AddNew(session, params)
            await session.close()
        except IntegrityError:
            logging.warning("Init User already created!")
