"""Atom controllers."""
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from data import Atom, Electron, Neutron, Proton
from data import (
    PydanticAtom,
    PydanticProton,
    PydanticElectron,
    PydanticNeutron,
)
from controllers import create_response, CurrentUser, CurrentSession

atom_router = APIRouter(prefix="/atoms", tags=["atoms"])


@atom_router.post("/create_atom")
async def create_atom(
    pydantic_atom: PydanticAtom,
    user: CurrentUser,
    session: CurrentSession,
) -> ORJSONResponse:
    """Create atom here."""

    atom = await Atom.AddNew(session, pydantic_atom.dict())

    await session.close()
    return create_response("Atom created succesfully!", atom.serialize(), 200)


@atom_router.post("/proton")
async def add_proton(
    pydantic_proton: PydanticProton,
    user: CurrentUser,
    session: CurrentSession,
) -> ORJSONResponse:
    """This controller creates a proton with the params received in the
    body."""

    proton = await Proton.AddNew(session, pydantic_proton.dict())

    return create_response(
        "Proton created succesfully!", proton.serialize(), 200
    )


@atom_router.get("/proton")
async def get_proton(
    user: CurrentUser,
    session: CurrentSession,
    pydantic_proton: PydanticProton = Depends(),
) -> ORJSONResponse:
    """Getting protons based on params."""

    protons = await Proton.GetByArgs(session, pydantic_proton.dict())
    protons = [proton.serialize() for proton in protons]

    await session.close()
    return create_response("Protons fetched!", 200, protons)


@atom_router.post("/neutron")
async def add_neutron(
    pydantic_neutron: PydanticNeutron,
    user: CurrentUser,
    session: CurrentSession,
) -> ORJSONResponse:
    """This controller creates a neutron with the params received in the
    body."""
    neutron = await Neutron.AddNew(session, pydantic_neutron.dict())

    await session.close()
    return create_response(
        "Neutron created succesfully!", 200, neutron.serialize()
    )


@atom_router.get("/neutron")
async def get_neutron(
    user: CurrentUser,
    session: CurrentSession,
    pydantic_neutron: PydanticNeutron = Depends(),
) -> ORJSONResponse:
    """Getting neutron based on params."""

    neutrons = await Neutron.GetByArgs(session, pydantic_neutron.dict())
    neutrons = [neutron.serialize() for neutron in neutrons]

    await session.close()
    return create_response("Protons fetched!", 200, neutrons)


@atom_router.post("/electron")
async def add_electron(
    pydantic_electron: PydanticElectron,
    user: CurrentUser,
    session: CurrentSession,
):
    """This controller creates a electron with the params received in the
    body."""

    electron = await Electron.AddNew(session, pydantic_electron.dict())

    await session.close()
    return create_response(
        "Electron created succesfully!", 200, electron.serialize()
    )


@atom_router.get("/electron")
async def get_electron(
    user: CurrentUser,
    session: CurrentSession,
    pydantic_electron: PydanticElectron = Depends(),
) -> ORJSONResponse:
    """Getting neutron based on params."""

    electrons = await Electron.GetByArgs(session, pydantic_electron.dict())
    electrons = [electron.serialize() for electron in electrons]

    await session.close()
    return create_response("Protons fetched!", 200, electrons)
