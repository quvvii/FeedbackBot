import logging
from aiogram import Bot, Router, exceptions
from aiogram.types import MessageReactionUpdated, ReactionTypeEmoji

from bot.config import settings
from bot.services.repo import Repo


logger = logging.getLogger(__name__)
router = Router(name="handle_reactions")


@router.message_reaction()
async def handle_reactions(
    event: MessageReactionUpdated,
    bot: Bot,
    repo: Repo,
) -> None:
    _reactions = [
        r for r in event.new_reaction
        if isinstance(r, ReactionTypeEmoji)
    ][:1]

    try:
        if event.user.id == settings.owner_id:
            target = await repo.message_relations.get_user_target(event.message_id)
            if not target:
                return

            await bot.set_message_reaction(
                chat_id=target["user_id"],
                message_id=target["user_message_id"],
                reaction=_reactions,
            )

        else:
            admin_msg_id = await repo.message_relations.get_admin_target(
                user_id=event.user.id,
                user_message_id=event.message_id,
            )
            if not admin_msg_id:
                return

            await bot.set_message_reaction(
                chat_id=settings.owner_id,
                message_id=admin_msg_id,
                reaction=_reactions,
            )

    except exceptions.TelegramBadRequest as e:
        logger.warning("Failed to sync reaction: %s", e)
    except exceptions.TelegramAPIError as e:
        logger.error("API error while syncing reaction: %s", e)
