from datetime import datetime
from enum import Enum

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, root_validator, Field

from ..common.models import UserBase
from ..db import groups

router = APIRouter(
    prefix='/groups',
    tags=['groups']
)


class GroupMember(UserBase):
    user_id: str = Field(alias='_id')


class GroupType(str, Enum):
    PERSONAL = "PERSONAL"
    MULTI_PARTICIPANTS = "MULTI_PARTICIPANTS"


class NewGroup(BaseModel):
    name: str | None = None
    type: GroupType
    members: list[GroupMember] = []
    created_at: datetime = datetime.now()

    @root_validator
    def check_required(cls, values):
        if values['type'] == GroupType.MULTI_PARTICIPANTS and not values.get('name'):
            raise ValueError('Multi participants group must have a name')
        elif values['type'] == GroupType.PERSONAL and values.get('name'):
            raise ValueError("Personal group doesn't have a name")
        return values


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_group(group: NewGroup):
    return await groups.create_group(jsonable_encoder(group))


@router.put("/{group_id}")
async def add_member(member: GroupMember, group_id: str):
    user_already_in_group = await groups.does_user_in_group(member.user_id, group_id)
    if user_already_in_group:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    await groups.add_user(member.user_id, group_id)
