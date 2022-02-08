"""
Basic controllers for users
"""

from typing import Dict

from fastapi import APIRouter, Depends, Request
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from data import User, get_session

from controllers import create_bulk_users, auth_decorator, create_response, parse
from utils import create_access_token, get_password_hash, verify_password


user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/create_users/{quantity}")
@auth_decorator
async def create_users(
    quantity: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    creates simple users in the database
    """
    params = await parse(request)
    if params:
        return create_response("Do not send params for this endpoint!", 400)
    await create_bulk_users(quantity, session)
    return create_response("Users created succesfully!", 200)


@user_router.post("/create_user")
@auth_decorator
async def create_user(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    creating a simple user
    """
    params = await parse(request)
    try:
        user = await User.AddNew(session, params)
    except Exception as e:
        return create_response(str(e), 400)

    return create_response("User created!", 200, user.to_dict())


@user_router.get("/get_user/{id_user}")
@auth_decorator
async def get_user(
    id_user: int, request: Request, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    """
    get user by id
    """
    params = await parse(request)
    if params:
        return create_response("No params needed on this endpoint!", 400)
    user = await User.GetById(id_user, session)

    return create_response("User fetched!", 200, user.to_dict())


@user_router.post("/login")
async def login(params: Dict[str, str], session: AsyncSession = Depends(get_session)):
    """
    login controller for a user
    """

    if "email" not in params:
        return create_response("Email is required", 400)
    if "password" not in params:
        return create_response("Password is required", 400)

    users = await User.GetByArgs(session, {"email": params["email"]})
    if len(users) > 1:
        return create_response("More than 1 user has the same email", 400)

    if not users:
        return create_response("No user with such email found", 400)

    user = users[0]

    if verify_password(params["password"], user.hashed_pass):
        token = create_access_token(params)
        return create_response(
            "User logged in!", 200, {"token": token, "user": user.to_dict()}
        )

    return create_response("Incorrect password!", 400)


@user_router.post("/sign-up")
async def sign_up(params: Dict[str, str], session: AsyncSession = Depends(get_session)):
    """
    Sign-up controller for the user
    """

    if "password" not in params:
        return create_response("Password is not present", 400)

    if "email" not in params:
        return create_response("Email address is not present", 400)

    if "username" not in params:
        return create_response("Username is not present", 400)

    password = params.pop("password")
    hashed_pass = await get_password_hash(password)
    params["hashed_pass"] = hashed_pass

    try:
        user = await User.AddNew(session, params)
    except Exception as user_error:
        return create_response(str(user_error), 400)

    return create_response("User created!", 200, user.to_dict())
