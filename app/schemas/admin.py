from pydantic import BaseModel
from enum import Enum


class Role(str, Enum):
    user = "user"
    moderator = "moderator"
    admin = "admin"


class Status(str, Enum):
    active = "active"
    banned = "banned"


class UserStatusUpdate(BaseModel):
    role: Role
    status: Status
