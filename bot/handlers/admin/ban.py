import logging
from aiogram import Bot, Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as hd

from bot.services.repo import Repo


logger = logging.getLogger(__name__)
router = Router()


async def target_user_id(
    msg: Message,
    command: CommandObject,
    repo: Repo,
) -> int | None:
    if command.args and command.args.isdigit():
        return int(command.args)

    if msg.reply_to_message:
        return await repo.message_relations.get_user_id_by_message(
            message_id=msg.reply_to_message.message_id
        )

    return None


@router.message(Command("ban"))
async def handle_ban_command(
    msg: Message,
    bot: Bot,
    command: CommandObject,
    repo: Repo,
) -> None:
    target_id = await target_user_id(msg, command, repo)
    if not target_id:
        await msg.reply("❌ Provide a valid User ID or reply to a ticket message.")
        return

    user = await repo.users.get_user(target_id)
    if not user:
        await msg.reply(f"❌ User with ID {hd.code(target_id)} not found.")
        return

    if user["is_banned"]:
        await msg.reply(f"ℹ️ User {hd.code(target_id)} is already banned.")
        return

    await repo.users.set_ban_status(user_id=target_id, is_banned=True)
    await msg.answer(f"🚫 User {hd.code(target_id)} has been banned.")


@router.message(Command("unban"))
async def handle_unban_command(
    msg: Message,
    bot: Bot,
    command: CommandObject,
    repo: Repo,
) -> None:
    target_id = await target_user_id(msg, command, repo)
    if not target_id:
        await msg.reply("❌ Provide a valid User ID or reply to a ticket message.")
        return

    user = await repo.users.get_user(target_id)
    if not user:
        await msg.reply(f"❌ User with ID {hd.code(target_id)} not found in database.")
        return

    if not user["is_banned"]:
        await msg.reply(f"ℹ️ User {hd.code(target_id)} is not banned.")
        return

    await repo.users.set_ban_status(user_id=target_id, is_banned=False)
    await msg.answer(f"✅ User {hd.code(target_id)} has been unbanned.")
