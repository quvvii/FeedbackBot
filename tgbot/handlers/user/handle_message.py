from aiogram import types, Router, Bot, F
from aiogram.utils.markdown import html_decoration as hd

from tgbot.database.repositories import MessageRelationsRepository
from tgbot.database.schemas import User

from tgbot.utils import time_ago

import config

import logging


logger = logging.getLogger(__name__)
router = Router()


@router.message(~F.text.startswith("/"))
async def forward_user_message_to_admin(
    msg: types.Message,
    bot: Bot,
    mr: MessageRelationsRepository,
    user: User
):
    tg_user = msg.from_user
    username = f"Username: @{tg_user.username}\n" if tg_user.username else ""

    user_info = (
        f"User: {tg_user.mention_html()}\n"
        f"ID: {hd.code(tg_user.id)}\n"
        f"{username}"
        f"Created {time_ago(user.created_at)}" if user else ""
    )

    info_msg = await bot.send_message(config.ADMIN_ID, user_info)

    try:
        if msg.video_note:
            sent_msg = await bot.send_video_note(
                chat_id=config.ADMIN_ID,
                video_note=msg.video_note.file_id
            )
        elif msg.voice:
            sent_msg = await bot.send_voice(
                chat_id=config.ADMIN_ID,
                voice=msg.voice.file_id,
                caption=msg.caption
            )
        else:
            sent_msg = await msg.send_copy(config.ADMIN_ID)

        await mr.create_relation(
            message_id=sent_msg.message_id,
            user_id=tg_user.id
        )

        await mr.create_relation(
            message_id=info_msg.message_id,
            user_id=tg_user.id
        )

    except Exception as e:
        logger.error(f"Forward error: {e}")
        await msg.reply("❌ Couldn't send message.")
