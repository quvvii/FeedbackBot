from typing import Any, Awaitable, Callable
from cachetools import TTLCache
from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 0.7) -> None:
        self.cache: TTLCache = TTLCache(maxsize=10_000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        if not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id
        if user_id in self.cache:
            return

        self.cache[user_id] = None
        return await handler(event, data)
