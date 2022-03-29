"""
api controllers
"""
from fastapi import Request
from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession


from data import get_session
from data import Atom, Electron, Neutron, Proton
from controllers import create_response, auth_decorator, parse

api_router = APIRouter(prefix="/api", tags=["api"])


@api_router.post("/external")
@auth_decorator
async def api_request(
    request: Request, session: AsyncSession = Depends(get_session)
) -> ORJSONResponse:
    """
    make a http request to an external api
    """

    params = await parse(request)

    return create_response("api called", 200)
