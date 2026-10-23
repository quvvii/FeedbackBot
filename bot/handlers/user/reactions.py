import logging
from aiogram import Bot, Router, types
from aiogram.exceptions import TelegramAPIError

from bot.config import settings
from bot.services.repo import Repo


logger = logging.getLogger(__name__)
router = Router(name="handle_reactions")


@router.message_reaction()
async def handle_reaction(
    event: types.MessageReactionUpdated,
    bot: Bot,
    repo: Repo,
) -> None:
    safe_reactions = [
        r for r in event.new_reaction
        if isinstance(r, types.ReactionTypeEmoji)
    ][:1]
    if not safe_reactions:
        return

    if event.chat.id == settings.owner_id:
        if not event.user or event.user.id != settings.owner_id:
            return

        relation = await repo.message_relations.get_by_topic_message(event.message_id)
        if not relation:
            return

        try:
            await bot.set_message_reaction(
                chat_id=relation["user_id"],
                message_id=relation["user_message_id"],
                reaction=safe_reactions,
            )
        except TelegramAPIError as e:
            logger.warning("Failed to sync reaction to user: %s", e)

    else:
        user = await repo.users.get_by_user_id(event.chat.id)
        if not user:
            return

        topic_msg_id = await repo.message_relations.get_by_user_message(
            user_id=user["user_id"],
            user_message_id=event.message_id,
        )
        if not topic_msg_id:
            return

        try:
            await bot.set_message_reaction(
                chat_id=settings.owner_id,
                message_id=topic_msg_id,
                reaction=safe_reactions,
            )
        except TelegramAPIError as e:
            logger.warning("Failed to sync reaction to topic: %s", e)
