"""Api controllers."""

from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

from controllers import CurrentUser, IcebergCatalog, create_response
from data import BaseResponse
from logger import log

iceberg_router = APIRouter(prefix="/iceberg", tags=["iceberg"])


@log()
@iceberg_router.get("/iceberg", response_model=BaseResponse)
async def api_request(_: CurrentUser, catalog: IcebergCatalog) -> ORJSONResponse:
    """Execute a query to the iceberg catalog."""

    result = catalog.list_namespaces()

    return create_response(
        message="Iceberg catalog called",
        status=status.HTTP_200_OK,
        response_model=BaseResponse,
        item=str(result),
    )
