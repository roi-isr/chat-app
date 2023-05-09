from . import db_connection
from .utils import to_object_id

groups_collection = db_connection.groups
users_collection = db_connection.users


async def does_user_in_group(user_id: str, group_id: str):
    group = await groups_collection.find_one({'_id': to_object_id(group_id)})
    if not group:
        return False
    group_member_ids = [member['_id'] for member in group['members']]
    return to_object_id(user_id) in group_member_ids


async def create_group(group: dict):
    result = await groups_collection.insert_one(group)
    return str(result.inserted_id)


async def add_user(user_id: str, group_id: str):
    user = await users_collection.find_one({'_id': to_object_id(user_id)},
                                           {'first_name': 1, 'last_name': 1})
    await groups_collection.update_one({"_id": to_object_id(group_id)},
                                       {"$push": {"members": user}})
