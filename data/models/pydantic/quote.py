from pydantic import BaseModel


class PydanticQuote(BaseModel):
    quote: str
    author: str
