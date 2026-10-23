from html import escape

from aiogram import Router, types
from aiogram.filters import Command

from bot.config import settings
from bot.services.repo import Repo


router = Router(name="handle_ban_command")


@router.message(Command("ban"))
async def ban_command(msg: types.Message, repo: Repo) -> None:
    if not msg.message_thread_id or msg.message_thread_id == 1:
        await msg.reply("Use this command inside a user thread.")
        return

    user = await repo.users.get_by_topic_id(msg.message_thread_id)
    if not user:
        return

    await repo.users.set_banned(user["user_id"], is_banned=True)
    await msg.reply(f"🚫 User <b>{escape(user['full_name'])}</b> (<code>{user['user_id']}</code>) banned.")


@router.message(Command("unban"), lambda m: m.chat.id == settings.owner_id)
async def unban_command(msg: types.Message, repo: Repo) -> None:
    if not msg.message_thread_id or msg.message_thread_id == 1:
        await msg.reply("Use this command inside a user thread.")
        return

    user = await repo.users.get_by_topic_id(msg.message_thread_id)
    if not user:
        return

    await repo.users.set_banned(user["user_id"], is_banned=False)
    await msg.reply(f"✅ User <b>{escape(user['full_name'])}</b> (<code>{user['user_id']}</code>) unbanned.")
