from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data.models import get_session
from controllers import create_response_ok, create_response_bad
from utils import oauth2_scheme, authenthicate_user

from data import Atom

atom_router = APIRouter(prefix="/atoms",
    tags=["atoms"])


@atom_router.post("/create_atom", )
async def create_atom(params: Dict[str, int], session: AsyncSession = Depends(get_session),\
    token: str = Depends(oauth2_scheme)):

    if not await authenthicate_user(token, session):
        return create_response_bad("Token expired! Please login again!")

    atom = await Atom.AddNew(session, params)
    await session.close()

    return create_response_ok("Atom created succesfully!", atom.to_dict())