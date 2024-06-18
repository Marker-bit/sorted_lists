import tinydb


async def get_db():
    database = tinydb.TinyDB("database.json")
    yield database
