from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import LinkPreviewOptions, Message
from aiogram.utils.markdown import html_decoration as hd

router = Router(name="start_user_cmd")


@router.message(CommandStart())
async def start_user_cmd(msg: Message) -> None:
    link_preview = LinkPreviewOptions(
        url="https://i.ibb.co/xS5qbKRy/83.png",
        show_above_text=True,
        prefer_large_media=True,
    )

    await msg.answer(
        f"Hello there, {hd.bold(msg.from_user.full_name)}!\n\n"
        f"What do you want?",
        link_preview_options=link_preview,
    )
