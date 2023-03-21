"""Basic controllers for users."""

from typing import Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import ORJSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from data import User, get_async_session

from controllers import create_response, parse, CurrentUser
from utils import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from utils.requests_parser import request_body_extraction


user_router = APIRouter(prefix="/users", tags=["users"])
templates = Jinja2Templates(directory="templates")


@user_router.post("/create_user")
async def create_user(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
):
    """Creating a simple user."""
    params = await parse(request)
    try:
        user = await User.AddNew(session, params)
    except Exception as e:
        return create_response(str(e), 400)

    return create_response("User created!", 200, user.serialize())


@user_router.get("/get_user/{id_user}")
async def get_user(
    id_user: int,
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """Get user by id."""
    await parse(request)
    user = await User.GetById(session, id_user)

    if not user:
        return create_response("User not found!", 400)

    return create_response("User fetched!", 200, user.serialize())


@user_router.post("/login")
async def login(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """Login controller for a user."""

    params = await request_body_extraction(request)

    if "email" not in params:
        return create_response("Email is required", 400)
    if "password" not in params:
        return create_response("Password is required", 400)

    users = await User.GetByArgs(session, {"email": params["email"]})

    if not users:
        return create_response("No user with such email found", 400)

    user = users[0]

    if verify_password(params["password"], user.hashed_pass):
        data = user.serialize()
        data.pop("id")
        data.pop("created_at")
        data.pop("updated_at")
        token = create_access_token(data)
        return create_response(
            "User logged in!", 200, {"token": token, "user": user.serialize()}
        )

    return create_response("Incorrect password!", 400)


@user_router.post("/sign-up")
async def sign_up(
    params: Dict[str, str],
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """Sign-up controller for the user."""

    if "password" not in params:
        return create_response("Password is not present", 400)

    if "email" not in params:
        return create_response("Email address is not present", 400)

    if "username" not in params:
        return create_response("Username is not present", 400)

    password = params.pop("password")
    hashed_pass = get_password_hash(password)
    params["hashed_pass"] = hashed_pass

    try:
        user = await User.AddNew(session, params)
    except Exception as user_error:
        return create_response(str(user_error), 400)

    return create_response("User created!", 200, user.serialize())
