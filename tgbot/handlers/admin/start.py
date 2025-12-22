from aiogram import Router, filters, types
from aiogram.utils.markdown import html_decoration as hd

from datetime import datetime
import time

from tgbot.database.repositories import UserRepository


router = Router()

@router.message(filters.Command("start"))
async def handle_start_admin_cmd(
        msg: types.Message,
        uptime: datetime,
        us: UserRepository
):
    diff = hd.code(str(datetime.now() - uptime).split(".")[0])

    total_users = hd.code(await us.total())
    total_banned = hd.code(await us.total_banned())

    start = time.perf_counter()
    original_msg = await msg.answer('\U0001F314')
    end = time.perf_counter()

    ping = hd.code(str(1000 * float(end - start)).split('.')[0] + 'ms')

    await original_msg.edit_text(
        text=f"{hd.italic('Bot is working!')}\n\n"
             f"{hd.bold('Total users for now:')} {total_users}\n"
             f"{hd.bold('Banned users for now:')} {total_banned}\n\n"
             f"{hd.bold('Uptime:')} {diff}\n"
             f"{hd.bold('Ping: ')} {ping}"
    )
