from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def ban_kb(user_id: int, is_banned: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    text = "🟢 Unban" if is_banned else "🔴 Ban"
    action = "unban" if is_banned else "ban"

    builder.button(
        text=text,
        callback_data=f"ban:{user_id}:{action}",
    )
    return builder.as_markup()
