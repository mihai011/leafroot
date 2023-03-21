"""atom controllers."""
from fastapi import Request, APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from data import get_async_session
from data import Atom, Electron, Neutron, Proton
from controllers import create_response, parse, CurrentUser

atom_router = APIRouter(prefix="/atoms", tags=["atoms"])


@atom_router.post("/create_atom")
async def create_atom(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """Create atom here."""
    params = await parse(request)
    atom = await Atom.AddNew(session, params)

    await session.close()
    return create_response("Atom created succesfully!", atom.serialize(), 200)


@atom_router.post("/proton")
async def add_proton(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """This controller creates a proton with the params received in the
    body."""
    params = await parse(request)
    proton = await Proton.AddNew(session, params)

    await session.close()
    return create_response(
        "Proton created succesfully!", proton.serialize(), 200
    )


@atom_router.get("/proton")
async def get_proton(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """Getting protons based on params."""

    params = await parse(request)
    params["charge"] = float(params["charge"])
    protons = await Proton.GetByArgs(session, params)
    protons = [proton.serialize() for proton in protons]

    await session.close()
    return create_response("Protons fetched!", 200, protons)


@atom_router.post("/neutron")
async def add_neutron(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """This controller creates a neutron with the params received in the
    body."""
    params = await parse(request)
    neutron = await Neutron.AddNew(session, params)

    await session.close()
    return create_response(
        "Neutron created succesfully!", 200, neutron.serialize()
    )


@atom_router.get("/neutron")
async def get_neutron(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """Getting neutron based on params."""

    params = await parse(request)
    params["charge"] = float(params["charge"])
    neutrons = await Neutron.GetByArgs(session, params)
    neutrons = [neutron.serialize() for neutron in neutrons]

    await session.close()
    return create_response("Protons fetched!", 200, neutrons)


@atom_router.post("/electron")
async def add_electron(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
):
    """This controller creates a electron with the params received in the
    body."""
    params = await parse(request)
    electron = await Electron.AddNew(session, params)
    # await session.close()

    await session.close()
    return create_response(
        "Electron created succesfully!", 200, electron.serialize()
    )


@atom_router.get("/electron")
async def get_electron(
    request: Request,
    user: CurrentUser,
    session: AsyncSession = Depends(get_async_session),
) -> ORJSONResponse:
    """Getting neutron based on params."""

    params = await parse(request)
    params["charge"] = float(params["charge"])
    electrons = await Electron.GetByArgs(session, params)
    electrons = [electron.serialize() for electron in electrons]

    await session.close()
    return create_response("Protons fetched!", 200, electrons)
