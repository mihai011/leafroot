"""Main module imported in the project.

Here you include the routers for the application and middleware used.
"""

import time

from fastapi import FastAPI, Request

from controllers.users_controllers import user_router
from controllers.base_controllers import base_router
from controllers.atom_controllers import atom_router
from controllers.api_controllers import api_router
from controllers.task_controllers import task_router

from cache import initialize_cache

app = FastAPI()


app.include_router(user_router)
app.include_router(atom_router)
app.include_router(base_router)
app.include_router(api_router)
app.include_router(task_router)

initialize_cache()


@app.middleware("http")
async def add_time_headers(request: Request, call_next):
    """Add time headers to check the time spent on the particular request."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
