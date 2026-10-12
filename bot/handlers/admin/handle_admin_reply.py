import logging
from aiogram import F, Router, exceptions
from aiogram.types import Message, ReactionTypeEmoji

from bot.services.repo import Repo


logger = logging.getLogger(__name__)
router = Router(name="handle_admin_reply")


@router.message(~F.text.startswith("/") & F.reply_to_message)
async def handle_admin_reply(
    msg: Message,
    repo: Repo,
) -> None:
    target_user_id = await repo.message_relations.get_user_id_by_message(
        message_id=msg.reply_to_message.message_id
    )

    if not target_user_id:
        await msg.reply("❌ Couldn't find the receiver for this message.")
        return

    try:
        sent_msg = await msg.send_copy(chat_id=target_user_id)
        await repo.message_relations.add_admin_reply(
            admin_message_id=msg.message_id,
            user_id=target_user_id,
            user_message_id=sent_msg.message_id,
        )

        if msg.reply_to_message:
            await msg.reply_to_message.react([ReactionTypeEmoji(emoji="👌")])

    except exceptions.TelegramForbiddenError:
        await msg.reply("❌ Delivery failed: user has blocked the bot.")

    except exceptions.TelegramBadRequest as e:
        logger.warning("Bad request while replying to user %s: %s", target_user_id, e)
        await msg.reply(f"❌ Delivery failed: {e.message}")

    except Exception as e:
        logger.error("Reply error to user %s: %s", target_user_id, e, exc_info=True)
        await msg.reply(f"❌ Unexpected error: {e}")
