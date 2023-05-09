from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from ..db import messages, groups

router = APIRouter(
    prefix='/messages',
    tags=['messages']
)


class NewMessage(BaseModel):
    message: str
    sender: str
    receiver: str
    created_at: datetime = datetime.now()


@router.get("/")
async def get_messages(group_id: str):
    return await messages.get_messages(group_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_message(message: NewMessage, group_id: Annotated[str, Body()]):
    for user_id in [message.sender, message.receiver]:
        users_in_group = await groups.does_user_in_group(user_id, group_id)
        if not users_in_group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"User {user_id} wasn't found in group {group_id}")

    message_id = await messages.create_message(jsonable_encoder(message), group_id)
    return {"MessageId": message_id}
