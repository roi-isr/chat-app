import bson
from bson import ObjectId


def to_object_id(str_):
    try:
        return ObjectId(str_)
    except bson.errors.InvalidId:
        raise ValueError(f'{str_} is an invalid Object ID')
