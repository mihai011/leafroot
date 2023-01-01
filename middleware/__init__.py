"""
Middleware module.
"""

import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimeRequestMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        """Add time headers to check the time spent on the particular request."""
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
