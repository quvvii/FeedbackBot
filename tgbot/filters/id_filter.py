from aiogram.filters import BaseFilter
from aiogram.types import Message

import config


class IDFilter(BaseFilter):
    def __init__(self, user_id: int = config.ADMIN_ID):
        self.user_id = user_id

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == self.user_id
