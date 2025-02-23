"""Api controllers."""

from venv import create
from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import create_response, CurrentUser, IcebergCatalog
from data import HttpRequest, BaseResponse
from utils.external_api import make_api_request
from logger import log

iceberg_router = APIRouter(prefix="/iceberg", tags=["iceberg"])


@log()
@iceberg_router.get("/iceberg", response_model=BaseResponse)
async def api_request(
    _: CurrentUser, catalog: IcebergCatalog
) -> ORJSONResponse:
    """Execute a query to the iceberg catalog."""

    result = catalog.list_namespaces()

    return create_response(
        message="Iceberg catalog called",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item=str(result),
    )
