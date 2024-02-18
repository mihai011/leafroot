"""Main module imported in the project.

Here you include the routers for the application and middleware used.
"""

from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.middleware import Middleware
from starlette_context import plugins
from starlette_context.middleware import RawContextMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import sentry_sdk

from controllers.users_controllers import user_router
from controllers.base_controllers import base_router
from controllers.atom_controllers import atom_router
from controllers.api_controllers import api_router
from controllers.task_controllers import task_router
from controllers.ws_controllers import ws_router
from controllers.utils_controllers import utils_router
from controllers.library_controllers import library_router
from controllers.quote_controllers import quotes_router
from controllers.cassandradb_controllers import cassandra_router
from controllers.url_controllers import url_router
from controllers.photo_controllers import photo_router
from data import async_session, User, create_database_app
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


# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    _: Request, exc: RequestValidationError
):
    """Error handler for Request package."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(_: Request, exc: HTTPException):
    """Error handler for HTTPException"""
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder({"detail": exc.detail}),
    )


@app.exception_handler(IntegrityError)
async def treat_integrity_error(_: Request, exc: IntegrityError):
    """Error handler for Integrity error."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": "Integrity Error!"}),
    )


if config.env not in ["dev", "circle"]:
    sentry_sdk.init(
        dsn=config.sentry_dsn,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )


# include routes
app.include_router(user_router)
app.include_router(atom_router)
app.include_router(base_router)
app.include_router(api_router)
app.include_router(task_router)
app.include_router(ws_router)
app.include_router(utils_router)
app.include_router(library_router)
app.include_router(quotes_router)
app.include_router(cassandra_router)
app.include_router(url_router)
app.include_router(photo_router)


@app.on_event("startup")
async def user_on_startup(session: AsyncSession = async_session()):
    """Creates a user at startup.

    Args:
        session (AsyncSession, optional): _description_. Defaults to Depends(get_async_session).
    """

    initialize_cache()
    initialize_logger()
    create_database_app()

    from logger import logger

    # initiate_cassandra()

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
            logger.warning("Init User already created!")
