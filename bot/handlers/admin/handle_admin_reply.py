import logging
from aiogram import Bot, F, Router, types
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError

from bot.config import settings
from bot.keyboards.admin import ban_kb
from bot.services.repo import Repo


logger = logging.getLogger(__name__)
router = Router(name="handle_admin_reply")


@router.message(F.message_thread_id, ~F.text.func(lambda t: t and t.startswith("/")))
async def handle_admin_reply(
    msg: types.Message,
    repo: Repo,
) -> None:
    if msg.message_thread_id == 1:
        return

    user = await repo.users.get_by_topic_id(msg.message_thread_id)
    if not user:
        return

    try:
        reply_msg_id = None
        if msg.reply_to_message:
            relation = await repo.message_relations.get_by_topic_message(
                topic_message_id=msg.reply_to_message.message_id
            )
            if relation:
                reply_msg_id = relation["user_message_id"]

        sent = await msg.send_copy(
            chat_id=user["user_id"],
            reply_parameters=(
                types.ReplyParameters(message_id=reply_msg_id)
                if reply_msg_id
                else None
            ),
        )

        await repo.message_relations.add_relation(
            user_id=user["user_id"],
            user_message_id=sent.message_id,
            topic_message_id=msg.message_id,
        )
    except TelegramForbiddenError:
        await msg.reply(
            "🚫 <b>User blocked the bot.</b>\n"
            "The message could not be delivered. You can close this ticket."
        )

    except TelegramAPIError as e:
        logger.error("Failed to deliver admin reply to user %s: %s", user["user_id"], e)
        await msg.reply(f"❌ Failed to send message: {e.message}")


@router.callback_query(F.data.startswith("ban:"))
async def handle_ban_callback(
    callback: types.CallbackQuery,
    repo: Repo,
) -> None:
    if not callback.data or not callback.message:
        await callback.answer()
        return

    _, user_id_str, action = callback.data.split(":", 2)
    user_id = int(user_id_str)
    new_action = action == "ban"

    await repo.users.set_banned(user_id=user_id, is_banned=new_action)

    await callback.message.edit_reply_markup(
        reply_markup=ban_kb(user_id, is_banned=new_action)
    )

    alert_text = f"User {user_id} banned." if new_action else f"User {user_id} unbanned."
    await callback.answer(text=alert_text, show_alert=True)
