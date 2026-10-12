import time
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import html_decoration as hd

from bot.services.repo import Repo
from bot.services.uptime import BotUptime

router = Router(name="start_admin_cmd")


@router.message(CommandStart())
async def start_admin_cmd(
    msg: Message,
    repo: Repo,
    uptime: BotUptime,
) -> None:
    t0 = time.perf_counter()
    await msg.bot.get_me()
    t1 = time.perf_counter()
    ping_ms = round((t1 - t0) * 1000)

    total_users = await repo.users.total()
    total_banned = await repo.users.total_banned()

    await msg.answer_sticker("CAACAgEAAxkBAAESB_5qzUIBu4Yt0KSQMn3Q1u8j8oUe7QACvAIAAiMGUUQSMTa4mm0Wjz0E")
    await msg.answer(
        f"<b>Users:</b>\n"
        f"├ Total: {hd.code(total_users)}\n"
        f"└ Banned: {hd.code(total_banned)}\n\n"
        f"<b>System:</b>\n"
        f"├ Uptime: {hd.code(uptime.formatted_uptime)}\n"
        f"└ Latency: {hd.code(f'{ping_ms}ms')}"
    )
