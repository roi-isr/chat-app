import datetime
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, status, Body, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, root_validator, Field

from .db import users, messages, groups


class UserBase(BaseModel):
    first_name: str
    last_name: str


class NewUser(UserBase):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    joined_at: datetime.datetime = datetime.datetime.now()
    groups: list = []


class GroupMember(UserBase):
    user_id: str = Field(alias='_id')


class NewMessage(BaseModel):
    message: str
    sender: str
    receiver: str
    created_at: datetime.datetime = datetime.datetime.now()


class GroupType(str, Enum):
    PERSONAL = "PERSONAL"
    MULTI_PARTICIPANTS = "MULTI_PARTICIPANTS"


class NewGroup(BaseModel):
    name: str | None = None
    type: GroupType
    members: list[GroupMember] = []
    created_at: datetime.datetime = datetime.datetime.now()

    @root_validator
    def check_required(cls, values):
        if values['type'] == GroupType.MULTI_PARTICIPANTS and not values.get('name'):
            raise ValueError('Multi participants group must have a name')
        elif values['type'] == GroupType.PERSONAL and values.get('name'):
            raise ValueError("Personal group doesn't have a name")
        return values


app = FastAPI()


@app.middleware('http')
async def error_handler(request: Request, call_next):
    try:
        response = await call_next(request)
    except ValueError as ex:
        return JSONResponse(content=str(ex), status_code=status.HTTP_400_BAD_REQUEST)
    return response


@app.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user: NewUser):
    user_id = await users.create_user(jsonable_encoder(user))
    return {"UserId": user_id}


@app.get("/messages")
async def get_messages(group_id: str):
    return await messages.get_messages(group_id)


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(message: NewMessage, group_id: Annotated[str, Body()]):
    for user_id in [message.sender, message.receiver]:
        users_in_group = await groups.does_user_in_group(user_id, group_id)
        if not users_in_group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User {user_id} wasn't found in group {group_id}")

    message_id = await messages.create_message(jsonable_encoder(message), group_id)
    return {"MessageId": message_id}


@app.post("/group", status_code=status.HTTP_201_CREATED)
async def create_group(group: NewGroup):
    return await groups.create_group(jsonable_encoder(group))


@app.put("/group/{group_id}")
async def add_member(member: GroupMember, group_id: str):
    user_already_in_group = await groups.does_user_in_group(member.user_id, group_id)
    if user_already_in_group:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    await groups.add_user(member.user_id, group_id)
