"""Library Controllers"""

from fastapi import APIRouter
from fastapi.responses import ORJSONResponse


from controllers import create_response, CurrentUser, MongoDatabase
from data import Library, BookPackage

library_router = APIRouter(prefix="/library", tags=["library"])


@library_router.post("/book")
async def add_book(_: CurrentUser, mongo_db: MongoDatabase, book: BookPackage):

    response = await Library.AddItem(mongo_db, book)
    return create_response("Book added!", 200)
