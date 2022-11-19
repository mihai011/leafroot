"""Main module imported in the project.

Here you include the routers for the application and middleware used.
"""

import time

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.users_controllers import user_router
from controllers.base_controllers import base_router
from controllers.atom_controllers import atom_router
from controllers.api_controllers import api_router
from controllers.task_controllers import task_router
from controllers.ws_controllers import ws_router
from controllers.utils_controllers import utils_router
from data import async_session, User, create_database_app
from config import config
from cache import initialize_cache
from logger import initialize_logger
from utils import get_password_hash

middleware = [
    Middleware(
        RawContextMiddleware,
        plugins=(plugins.RequestIdPlugin(), plugins.CorrelationIdPlugin()),
    )
]


app = FastAPI(middleware=middleware)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(user_router)
app.include_router(atom_router)
app.include_router(base_router)
app.include_router(api_router)
app.include_router(task_router)
app.include_router(ws_router)
app.include_router(utils_router)

initialize_cache()
initialize_logger(config)
create_database_app(config.postgres_db)


@app.middleware("http")
async def add_time_headers(request: Request, call_next):
    """Add time headers to check the time spent on the particular request."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.on_event("startup")
async def user_on_startup(session: AsyncSession = async_session()):
    """Creates a user at startup

    Args:
        session (AsyncSession, optional): _description_. Defaults to Depends(get_session).
    """

    if config.user_name and config.user_email and config.user_password:
        params = {
            "username": config.user_name,
            "email": config.user_email,
        }

        user = await User.GetByArgs(session, params)
        if not user:
            hashed_pass = get_password_hash(config.user_password)
            params["hashed_pass"] = hashed_pass
            user = await User.AddNew(session, params)
            await session.close()
