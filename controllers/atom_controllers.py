from typing import Any, Dict
from typing import Optional
from fastapi import Request

from httpx import AsyncClient
from data.models.atom import Electron, Neutron, Proton

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import ORJSONResponse


from data.models import get_session
from controllers import create_response, auth_decorator
from utils import oauth2_scheme, authenthicate_user

from data import Atom

atom_router = APIRouter(prefix="/atoms", tags=["atoms"])


@atom_router.post("/create_atom")
@auth_decorator
async def create_atom(
    params: Dict[str, int],
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> ORJSONResponse:

    atom = await Atom.AddNew(session, params)
    await session.close()

    return create_response("Atom created succesfully!", atom.to_dict(), 200)


@atom_router.post("/proton")
@auth_decorator
async def add_proton(
    params: Dict[str, int],
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> ORJSONResponse:
    """
    This controller creates a proton with the params received in the body
    """

    proton = await Proton.AddNew(session, params)
    await session.close()

    return create_response("Proton created succesfully!", proton.to_dict())


@atom_router.get("/proton")
async def get_proton(
    req: Request,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    """
    Getting protons based on params
    """
    params = dict(req.query_params)
    protons = await Proton.GetByArgs(params)
    protons = [proton.to_dict() for proton in protons]

    return create_response("Protons fetched!", 200, protons)


@atom_router.post("/neutron")
@auth_decorator
async def add_neutron(
    params: Dict[str, int],
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
) -> ORJSONResponse:
    """
    This controller creates a neutron with the params received in the body
    """

    neutron = await Neutron.AddNew(session, params)
    await session.close()

    return create_response("Neutron created succesfully!", neutron.to_dict(), 200)


@atom_router.post("/electron")
@auth_decorator
async def add_electron(
    params: Dict[str, int],
    session: AsyncSession = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):

    """
    This controller creates a electron with the params received in the body
    """

    electron = await Electron.AddNew(session, params)
    await session.close()

    return create_response("Electron created succesfully!", electron.to_dict(), 200)
