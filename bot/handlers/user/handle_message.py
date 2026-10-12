from datetime import datetime, timezone
import logging
from aiogram import Bot, F, Router
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as hd
import aiosqlite

from bot.services.repo import Repo
from bot.config import settings


logger = logging.getLogger(__name__)
router = Router(name="handle_user_message")

_last_user_id: int | None = None


@router.message(~F.text.startswith("/"))
async def handle_user_message(
    msg: Message,
    bot: Bot,
    repo: Repo,
    user: aiosqlite.Row,
) -> None:
    global _last_user_id

    tg_user = msg.from_user
    if not tg_user:
        return

    try:
        if _last_user_id != tg_user.id:
            username_part = f"Username: @{tg_user.username}\n" if tg_user.username else ""

            dt = datetime.fromisoformat(user["created_at"]).replace(tzinfo=timezone.utc)
            reg_date = dt.astimezone(settings.tz).strftime("%H:%M %d.%m.%Y")

            user_info = (
                f"<b>New Message</b>\n"
                f"━━━━━━━━━━━━━━━━━━\n"
                f"From: {tg_user.mention_html()}\n"
                f"ID: {hd.code(tg_user.id)}\n"
                f"{username_part}"
                f"Registered: {reg_date}\n"
                f"━━━━━━━━━━━━━━━━━━"
            )

            info_msg = await bot.send_message(
                chat_id=settings.owner_id,
                text=user_info,
            )
            await repo.message_relations.add_user_message(
                admin_message_id=info_msg.message_id,
                user_id=tg_user.id,
                user_message_id=msg.message_id,
            )

        copied_msg = await msg.send_copy(chat_id=settings.owner_id)
        await repo.message_relations.add_user_message(
            admin_message_id=copied_msg.message_id,
            user_id=tg_user.id,
            user_message_id=msg.message_id,
        )

        _last_user_id = tg_user.id

    except Exception as e:
        logger.error("Failed to forward message from user %s: %s", tg_user.id, e, exc_info=True)
        await msg.reply("❌ Couldn't deliver your message. Please try again.")
