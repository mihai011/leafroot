from data.models.quote import Quote


async def get_random_quote(session):
    """Retreives a random Quote"""

    quote = await Quote.GetRandom(session)

    return quote
