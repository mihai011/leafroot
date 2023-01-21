"""Specific util functions for request parsing."""
from fastapi import Request
from logger import log


@log()
async def request_body_extraction(request: Request):
    """Extract the data from the request Body.

    Args:
        request (Request): Starlette Request object

    Returns:
        JSON: data from the request body
    """

    data = {}

    data = await request.form()
    if data._dict:
        return data._dict

    data = await request.json()

    return data
