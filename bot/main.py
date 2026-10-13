import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import ErrorEvent
from aiogram.client.session.aiohttp import AiohttpSession

from bot.config import settings
from bot.logger import setup_logging
from bot.handlers import get_handlers_router

from bot.middlewares.logging_mw import LoggingMiddleware
from bot.middlewares.throttling_mw import ThrottlingMiddleware
from bot.middlewares.db_session_mw import RepoMiddleware
from bot.middlewares.user_mw import UserMiddleware

from bot.services.db import init_db
from bot.services.repo import build_repo
from bot.services.uptime import BotUptime


logger = logging.getLogger(__name__)


async def main() -> None:
    setup_logging(settings.log_level)

    session = AiohttpSession(proxy=settings.proxy_url) if settings.proxy_url else None

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,
    )
    dp = Dispatcher()

    db = await init_db(settings.db_path)
    repo = build_repo(db)

    dp.update.outer_middleware(RepoMiddleware(repo))
    dp.update.outer_middleware(LoggingMiddleware())
    dp.message.middleware(ThrottlingMiddleware(rate_limit=0.7))
    dp.message.middleware(UserMiddleware())

    dp.include_router(get_handlers_router())

    @dp.errors()
    async def global_error_handler(event: ErrorEvent) -> bool:
        logger.exception(
            "Unhandled error during the update %s", event.update, exc_info=event.exception
        )
        return True

    try:
        await bot.delete_webhook(drop_pending_updates=True)

        dp["uptime"] = BotUptime()

        logger.info("Bot started")
        await dp.start_polling(
            bot,
            allowed_updates=[
                "message",
                "message_reaction",
                "callback_query",
            ],
        )

    finally:
        await db.close()
        await bot.session.close()
        logger.info("Bot stopped, connections closed")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
