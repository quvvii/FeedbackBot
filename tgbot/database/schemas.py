from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    id: int
    name: str
    is_banned: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MessageRelations(BaseModel):
    message_id: int
    user_id: int

    class Config:
        from_attributes = True
