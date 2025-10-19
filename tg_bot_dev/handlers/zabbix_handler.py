from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from tg_bot_dev.settings import settings
from tg_bot_dev.services import Parser

router = Router()


# --- Хелпер: проверка ACL ---
def is_allowed(msg: Message) -> bool:
    print(settings.acl_ids, f'Get message from {msg.from_user.id} it is in acl: {msg.from_user.id in settings.acl_ids}')
    uid = msg.from_user.id if msg.from_user else None
    return uid in settings.acl_ids


@router.message(Command("alerts"))
async def cmd_allerts_7(message: Message):
    z_parser = Parser()
    messages = z_parser.get_recent_problems(settings.zbx_uri, settings.zbx_user, settings.zbx_passwd)
    if not is_allowed(message):
        return
    await message.answer("Alerts: ")
    for m in messages:
       await message.answer(m)
