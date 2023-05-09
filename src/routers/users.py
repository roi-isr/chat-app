from datetime import datetime

from fastapi import APIRouter
from fastapi import status
from fastapi.encoders import jsonable_encoder

from ..common import models
from ..db import users

router = APIRouter(
    prefix='/users',
    tags=['users']
)


class NewUser(models.UserBase):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    joined_at: datetime = datetime.now()
    groups: list = []


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user: NewUser):
    user_id = await users.create_user(jsonable_encoder(user))
    return {"UserId": user_id}
