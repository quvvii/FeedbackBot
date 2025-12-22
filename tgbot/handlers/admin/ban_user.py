from aiogram import Router, types, filters
from aiogram.utils.markdown import html_decoration as hd

from tgbot.database.repositories import UserRepository
from tgbot.database.repositories import MessageRelationsRepository


router = Router()

@router.message(filters.Command("ban"))
async def handle_ban_user_cmd(
    msg: types.Message,
    us: UserRepository,
    mr: MessageRelationsRepository
):
    if msg.reply_to_message:
        relation = await mr.get_relation(msg.reply_to_message.message_id)

        if not relation:
            return await msg.reply("❌ Couldn't find this user.")

        user_id = relation.user_id

    else:
        sl = msg.text.split()

        if len(sl) == 2 and sl[1].isdigit():
            user_id = int(sl[1])
        else:
            return await msg.reply("❌ Couldn't find this user.")

    user = await us.get_user(user_id)

    if not user:
        return await msg.reply("❌ Couldn't find this user.")

    await us.update_user(user.id, True)
    await msg.reply(f"{hd.bold(user.name)} was banned.")


@router.message(filters.Command("unban"))
async def handle_unban_user_cmd(
        msg: types.Message,
        us: UserRepository,
        mr: MessageRelationsRepository
):
    if msg.reply_to_message:
        relation = await mr.get_relation(msg.reply_to_message.message_id)

        if not relation:
            return await msg.reply("❌ Couldn't find this user.")

        user_id = relation.user_id

    else:
        sl = msg.text.split()

        if len(sl) == 2 and sl[1].isdigit():
            user_id = int(sl[1])
        else:
            return await msg.reply("❌ Couldn't find this user.")

    user = await us.get_user(user_id)

    if not user:
        return await msg.reply("❌ Couldn't find this user.")

    await us.update_user(user.id, False)
    await msg.reply(f"{hd.bold(user.name)} was unbanned.")
