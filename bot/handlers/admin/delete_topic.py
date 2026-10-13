import logging
from aiogram import Bot, Router, types
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError

from bot.config import settings
from bot.services.repo import Repo


logger = logging.getLogger(__name__)
router = Router(name="admin_delete_topic")


@router.message(Command("close", "delete", "del"),)
async def cmd_delete_topic(
    msg: types.Message,
    bot: Bot,
    repo: Repo,
) -> None:
    if not msg.message_thread_id or msg.message_thread_id == 1:
        await msg.reply("❌ Cannot delete the General topic.")
        return

    topic_id = msg.message_thread_id

    await repo.users.clear_topic_id(topic_id)

    try:
        await bot.delete_forum_topic(
            chat_id=settings.owner_id,
            message_thread_id=topic_id,
        )
    except TelegramAPIError as e:
        logger.error("Failed to delete forum topic %s: %s", topic_id, e)
        await msg.reply(f"❌ Failed to delete topic: {e.message}")
