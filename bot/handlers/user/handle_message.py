import logging
from datetime import datetime, timezone
from aiogram import Bot, Router, types, F
from aiogram.utils.markdown import html_decoration as hd

from bot.config import settings
from bot.keyboards.admin import ban_kb
from bot.services.repo import Repo


logger = logging.getLogger(__name__)
router = Router(name="handle_user_message")


def format_topic_name(user_num: int, full_name: str, max_length: int = 128) -> str:
    raw_name = f"#{user_num} | {full_name}"
    if len(raw_name) <= max_length:
        return raw_name
    return raw_name[: max_length - 3] + "..."


@router.message(
    F.chat.id != settings.owner_id,
    ~F.from_user.is_bot,
    ~F.text.func(lambda t: t and t.startswith("/")),
)
async def handle_user_message(
    msg: types.Message,
    bot: Bot,
    repo: Repo,
) -> None:
    tg_user = msg.from_user
    user = await repo.users.get_or_create(
        user_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )

    topic_id = user["topic_id"]

    if not topic_id:
        try:
            topic = await bot.create_forum_topic(
                chat_id=settings.owner_id,
                name=format_topic_name(user['id'], tg_user.full_name)
            )
            topic_id = topic.message_thread_id
            await repo.users.set_topic_id(tg_user.id, topic_id)

            username = f"├ Username: @{tg_user.username}\n" if tg_user.username else ""

            dt = datetime.fromisoformat(user["created_at"]).replace(tzinfo=timezone.utc)
            reg_date = dt.astimezone(settings.tz).strftime("%H:%M %d.%m.%Y")

            user_info = (
                f"<b>Ticket #{user['id']}</b> {tg_user.mention_html()}\n"
                f"├ ID: <code>{tg_user.id}</code>\n"
                f"{username}"
                f"└ Registered: <code>{reg_date}</code>"
            )

            info_msg = await bot.send_message(
                chat_id=settings.owner_id,
                message_thread_id=topic_id,
                text=user_info,
                reply_markup=ban_kb(tg_user.id, is_banned=False),
            )

            await bot.pin_chat_message(
                chat_id=settings.owner_id,
                message_id=info_msg.message_id,
                disable_notification=True,
            )

            try:
                await bot.delete_message(
                    chat_id=settings.owner_id,
                    message_id=info_msg.message_id + 1,
                )
            except Exception:
                pass

        except Exception as e:
            logger.error("Failed to create topic or send info card: %s", e)
            await msg.answer("❌ Couldn't deliver your message. Please try again.")
            return

    try:
        reply_msg_id = None
        if msg.reply_to_message:
            reply_msg_id = await repo.message_relations.get_by_user_message(
                user_id=tg_user.id,
                user_message_id=msg.reply_to_message.message_id,
            )

        copied = await msg.send_copy(
            chat_id=settings.owner_id,
            message_thread_id=topic_id,
            reply_parameters=(
                types.ReplyParameters(message_id=reply_msg_id)
                if reply_msg_id
                else None
            ),
        )

        await repo.message_relations.add_relation(
            user_id=tg_user.id,
            user_message_id=msg.message_id,
            topic_message_id=copied.message_id,
        )
    except Exception as e:
        logger.error("Failed to forward user message: %s", e)
