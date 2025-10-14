from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot_dev.settings import settings


router = Router()


# --- Хелпер: проверка ACL ---
def is_allowed(msg: Message) -> bool:
    print(settings.acl_ids, f'Get message from {msg.from_user.id} it is in acl: {msg.from_user.id in settings.acl_ids}')
    uid = msg.from_user.id if msg.from_user else None
    return uid in settings.acl_ids


@router.message(Command("alerts"))
async def cmd_allerts_7(message: Message):
    if not is_allowed(message):
        return
    parts = [
        "1 msg",
        "2 msg",
        "3 msg"
    ]
    sent : list[Message] = []
    for p in parts:
        m = await message.answer(p)
        sent.append(m)
