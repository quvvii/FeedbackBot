from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser

from bot.services.repo import Repo


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        tg_user: TelegramUser | None = data.get("event_from_user")
        if not tg_user:
            return await handler(event, data)

        repo: Repo = data["repo"]

        user = await repo.users.get_or_create(
            user_id=tg_user.id,
            full_name=tg_user.full_name,
            username=tg_user.username,
        )

        if user["is_banned"]:
            return

        data["user"] = user

        return await handler(event, data)
