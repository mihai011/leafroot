"""
atom controllers
"""
from fastapi import Request
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from data.models.atom import Electron, Neutron, Proton
from data.models import get_session
from data import Atom
from controllers import create_response, auth_decorator, parse



atom_router = APIRouter(prefix="/atoms", tags=["atoms"])


@atom_router.post("/create_atom")
@auth_decorator
async def create_atom(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    """
    Create atom here
    """
    params = await parse(request)
    atom = await Atom.AddNew(session, params)
    await session.close()

    return create_response("Atom created succesfully!", atom.to_dict(), 200)


@atom_router.post("/proton")
@auth_decorator
async def add_proton(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    """
    This controller creates a proton with the params received in the body
    """
    params = await parse(request)
    proton = await Proton.AddNew(session, params)

    return create_response("Proton created succesfully!", proton.to_dict())


@atom_router.get("/proton")
@auth_decorator
async def get_proton(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    """
    Getting protons based on params
    """

    params = await parse(request)
    params["charge"] = float(params["charge"])
    protons = await Proton.GetByArgs(session, params)
    protons = [proton.serialize() for proton in protons]

    return create_response("Protons fetched!", 200, protons)


@atom_router.post("/neutron")
@auth_decorator
async def add_neutron(
    request: Request,
    session: AsyncSession = Depends(get_session),
) -> ORJSONResponse:
    """
    This controller creates a neutron with the params received in the body
    """
    params = await parse(request)
    neutron = await Neutron.AddNew(session, params)
    await session.close()

    return create_response("Neutron created succesfully!", neutron.to_dict(), 200)


@atom_router.post("/electron")
@auth_decorator
async def add_electron(
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    This controller creates a electron with the params received in the body
    """
    params = await parse(request)
    electron = await Electron.AddNew(session, params)
    await session.close()

    return create_response("Electron created succesfully!", electron.to_dict(), 200)
