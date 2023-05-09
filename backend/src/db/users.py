from . import db_connection

collection = db_connection.users


async def create_user(user: dict):
    result = await collection.insert_one(user)
    return str(result.inserted_id)
