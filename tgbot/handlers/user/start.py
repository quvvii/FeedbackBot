from aiogram import Router, filters, types
from aiogram.types.link_preview_options import LinkPreviewOptions
from aiogram.utils.markdown import html_decoration as hd


router = Router()


@router.message(filters.Command("start"))
async def handle_start_user_cmd(msg: types.Message):
    link_preview = LinkPreviewOptions(
        is_disabled=False,
        url="https://i.ibb.co/xS5qbKRy/83.png",
        show_above_text=True
    )

    await msg.answer(
        f"Hello there, {hd.bold(msg.from_user.full_name)}!\n"
        f"What do you want?",
        link_preview_options=link_preview
    )
