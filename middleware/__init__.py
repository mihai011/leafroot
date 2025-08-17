"""Middleware module."""

import time
from typing import Callable

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class TimeRequestMiddleware(BaseHTTPMiddleware):
    """Class for Middleware to set up time for requests."""

    def __init__(
        self,
        app: FastAPI,
    ) -> None:
        """Constructor for middleware class."""
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """Add time headers to check the time spent on the particular request."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
