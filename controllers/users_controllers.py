from typing import Any, Dict
from functools import wraps

from fastapi import Request
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import get_session
from controllers import create_bulk_users, auth_decorator, create_response
from utils import create_access_token, get_password_hash, verify_password, oauth2_scheme
from data import User

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/create_users/{quantity}")
@auth_decorator
async def create_users(
    quantity: int,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    await create_bulk_users(quantity, session)
    return create_response("Users created succesfully!", 200)


@user_router.post("/create_user")
@auth_decorator
async def create_user(
    params: Dict[str, str],
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    try:
        user = await User.AddNew(session, params)
    except Exception as e:
        return create_response(str(e), 400)

    return create_response("User created!", 200, user.to_dict())


@user_router.get(
    "/get_user/{id}",
)
async def create_users(
    id: int,
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    user = await User.GetById(id, session)

    return create_response("User fetched!", 200, user.to_dict())


@user_router.post("/login")
async def login(params: Dict[str, str], session: AsyncSession = Depends(get_session)):

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
    else:
        return create_response("Incorrect password!", 400)


@user_router.post("/sign-up")
async def sign_up(params: Dict[str, str], session: AsyncSession = Depends(get_session)):

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
    except Exception as e:
        return create_response(str(e), 400)

    return create_response("User created!", 200, user.to_dict())
