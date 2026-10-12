from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User as TelegramUser
import aiosqlite

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

        await repo.users.upsert_user(
            user_id=tg_user.id,
            name=tg_user.full_name,
            username=tg_user.username,
        )

        db_user: aiosqlite.Row | None = await repo.users.get_user(tg_user.id)

        if db_user and db_user["is_banned"]:
            return

        data["user"] = db_user

        return await handler(event, data)
