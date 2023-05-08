from . import db_connection
from .utils import to_object_id

messages_collection = db_connection.messages
groups_collection = db_connection.groups


async def get_messages(group_id: str):
    messages_refs = (await groups_collection.find_one({'_id': to_object_id(group_id)}, {"_id": 0, "messages_refs": 1}))[
        'messages_refs']
    messages = []
    for message_ref in messages_refs:
        message = await messages_collection.find_one({'_id': message_ref})
        message['_id'] = str(message['_id'])
        messages.append(message)
    return messages


async def create_message(message: dict, group_id: str):
    result = await messages_collection.insert_one(message)
    message_id = result.inserted_id
    await groups_collection.update_one({"_id": to_object_id(group_id)},
                                       {"$push": {"messages_refs": message_id}})
    return str(message_id)
