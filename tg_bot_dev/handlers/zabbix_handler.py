from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from tg_bot_dev.settings import settings
from tg_bot_dev.services import Parser
from tg_bot_dev.keyboards import main_menu


router = Router()


# --- Хелпер: проверка ACL ---
def is_allowed(msg: Message) -> bool:
    print(settings.acl_ids, f'Get message from {msg.from_user.id} it is in acl: {msg.from_user.id in settings.acl_ids}')
    uid = msg.from_user.id if msg.from_user else None
    return uid in settings.acl_ids

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Приветственное сообщение. Клавиатура только для ACL."""
    if not is_allowed(message):
        return

    await message.answer(
        "Привет!\nВыберите действие ниже:",
        reply_markup=main_menu
    )


# --- Общая логика отправки ---
async def send_alerts(message: Message, days: int):
    if not is_allowed(message):
        return
    z = Parser()
    msgs = z.get_recent_problems(settings.zbx_uri, settings.zbx_user, settings.zbx_passwd, days)

    if not msgs:
        await message.answer(f"Алертов за {days} дней нет ✅", reply_markup=main_keyboard)
        return

    await message.answer("Alerts:")
    for m in msgs:
        await message.answer(m)
    await message.answer("Готово. Возврат в главное меню ⬇️", reply_markup=main_keyboard)

# --- Команды ---
@router.message(F.text==("Alerts за 3 дня"))
async def cmd_alerts_3(message: Message):
    print("1")
    await send_alerts(message, 3)

@router.message(F.text==("Alerts за 7 дней"))
async def cmd_alerts_7(message: Message):
    await send_alerts(message, 7)

@router.message(F.text==("Alerts за 30 дней"))
async def cmd_alerts_30(message: Message):
    await send_alerts(message, 30)

@router.message(F.text==("Alerts за 90 дней"))
async def cmd_alerts_90(message: Message):
    await send_alerts(message, 90)

@router.message(F.text)
async def echo_log(message: Message):
    print(f"DEBUG got text: {repr(message.text)}")  # посмотри в консоли точную строку
    await message.answer("Неизвестная команда")
