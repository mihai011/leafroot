"""Atom controllers."""

from fastapi import APIRouter, status, Depends
from fastapi.responses import ORJSONResponse

from data import Atom, Electron, Neutron, Proton
from data import (
    PydanticAtom,
    PydanticProton,
    PydanticElectron,
    PydanticNeutron,
    AtomResponseItem,
    ParticleResponseItem,
    ParticleResponseListItem,
)
from controllers import create_response, CurrentUser, CurrentAsyncSession

atom_router = APIRouter(prefix="/atoms", tags=["atoms"])


@atom_router.post("/create_atom", response_model=AtomResponseItem)
async def create_atom(
    pydantic_atom: PydanticAtom,
    _: CurrentUser,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """Create atom here."""

    atom = await Atom.AddNew(session, pydantic_atom.model_dump())

    return create_response(
        message="Atom created succesfully!",
        status=status.HTTP_200_OK,
        response_model=AtomResponseItem,
        item=atom.serialize(),
    )


@atom_router.post("/proton", response_model=ParticleResponseItem)
async def add_proton(
    pydantic_proton: PydanticProton,
    _: CurrentUser,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """This controller creates a proton with the params received in the
    body."""

    proton = await Proton.AddNew(session, pydantic_proton.model_dump())

    return create_response(
        message="Proton created succesfully!",
        status=status.HTTP_200_OK,
        response_model=ParticleResponseItem,
        item=proton.serialize(),
    )


@atom_router.get("/proton", response_model=ParticleResponseListItem)
async def get_proton(
    _: CurrentUser,
    session: CurrentAsyncSession,
    pydantic_proton: PydanticProton = Depends(),
) -> ORJSONResponse:
    """Getting protons based on params."""

    protons = await Proton.GetByArgs(session, pydantic_proton.dict())
    protons = {"protons": [proton.serialize() for proton in protons]}

    return create_response(
        message="Protons fetched!",
        status=status.HTTP_200_OK,
        response_model=ParticleResponseListItem,
        item=protons,
    )


@atom_router.post("/neutron", response_model=ParticleResponseItem)
async def add_neutron(
    pydantic_neutron: PydanticNeutron,
    _: CurrentUser,
    session: CurrentAsyncSession,
) -> ORJSONResponse:
    """This controller creates a neutron with the params received in the
    body."""
    neutron = await Neutron.AddNew(session, pydantic_neutron.dict())

    return create_response(
        message="Neutron created succesfully!",
        status=status.HTTP_200_OK,
        response_model=ParticleResponseItem,
        item=neutron.serialize(),
    )


@atom_router.get("/neutron", response_model=ParticleResponseListItem)
async def get_neutron(
    _: CurrentUser,
    session: CurrentAsyncSession,
    pydantic_neutron: PydanticNeutron = Depends(),
) -> ORJSONResponse:
    """Getting neutron based on params."""

    neutrons = await Neutron.GetByArgs(session, pydantic_neutron.dict())
    neutrons = {"neutrons": [neutron.serialize() for neutron in neutrons]}

    return create_response(
        message="Neutrons fetched!",
        status=status.HTTP_200_OK,
        response_model=ParticleResponseListItem,
        item=neutrons,
    )


@atom_router.post("/electron", response_model=ParticleResponseItem)
async def add_electron(
    pydantic_electron: PydanticElectron,
    _: CurrentUser,
    session: CurrentAsyncSession,
):
    """This controller creates a electron with the params received in the
    body."""

    electron = await Electron.AddNew(session, pydantic_electron.dict())

    return create_response(
        message="Electron created succesfully!",
        status=status.HTTP_200_OK,
        response_model=ParticleResponseItem,
        item=electron.serialize(),
    )


@atom_router.get("/electron", response_model=ParticleResponseListItem)
async def get_electron(
    _: CurrentUser,
    session: CurrentAsyncSession,
    pydantic_electron: PydanticElectron = Depends(),
) -> ORJSONResponse:
    """Getting neutron based on params."""

    electrons = await Electron.GetByArgs(session, pydantic_electron.dict())
    electrons = {"electrons": [electron.serialize() for electron in electrons]}

    return create_response(
        message="Electrons fetched!",
        status=status.HTTP_200_OK,
        response_model=ParticleResponseListItem,
        item=electrons,
    )
