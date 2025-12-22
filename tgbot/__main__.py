import asyncio
import datetime
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

import config

from tgbot.logger import setup_logger
from tgbot.database import connect_database, close_connection
from tgbot.handlers import setup_routers
from tgbot.middlewares import setup_middlewares


class BotManager:
    def __init__(self):
        self.bot: Bot | None = None
        self.dp: Dispatcher | None = None

        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    async def setup(self):
        self.bot = Bot(token=self.config.TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
        self.dp = Dispatcher(storage=MemoryStorage())

        self.dp.startup.register(self.on_startup)
        self.dp.shutdown.register(self.on_shutdown)

    async def on_startup(self):
        self.dp['uptime'] = datetime.datetime.now()

        await connect_database()
        setup_routers(self.dp)
        setup_middlewares(self.dp)

        await self.bot.delete_webhook(drop_pending_updates=True)
        self.logger.info("Bot startup completed")

    async def on_shutdown(self):
        await close_connection()
        await self.bot.session.close()

        self.logger.info("Bot shutdown completed")

    async def run(self):
        await self.setup()

        try:
            self.logger.info("Starting bot...")
            await self.dp.start_polling(self.bot)

        except Exception as e:
            self.logger.critical(f"Fatal error: {e}", exc_info=True)

        finally:
            self.logger.info("Bot stopped")


async def main():
    setup_logger()

    manager = BotManager()
    await manager.run()


if __name__ == "__main__":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except AttributeError:
        pass

    asyncio.run(main())
