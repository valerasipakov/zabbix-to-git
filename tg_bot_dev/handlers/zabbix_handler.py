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
@router.message(Command("alerts_3"))
async def cmd_alerts_3(message: Message):
    await send_alerts(message, 3)

@router.message(Command("alerts_7"))
async def cmd_alerts_7(message: Message):
    await send_alerts(message, 7)

@router.message(Command("alerts_30"))
async def cmd_alerts_30(message: Message):
    await send_alerts(message, 30)

@router.message(Command("alerts_90"))
async def cmd_alerts_90(message: Message):
    await send_alerts(message, 90)

# --- Inline-кнопки (если используешь InlineKeyboardButton с такими callback_data) ---
@router.callback_query(F.data == "alerts_3")
async def cb_alerts_3(cq: CallbackQuery):
    await send_alerts(cq.message, 3)
    await cq.answer()

@router.callback_query(F.data == "alerts_7")
async def cb_alerts_7(cq: CallbackQuery):
    await send_alerts(cq.message, 7)
    await cq.answer()

@router.callback_query(F.data == "alerts_30")
async def cb_alerts_30(cq: CallbackQuery):
    await send_alerts(cq.message, 30)
    await cq.answer()

@router.callback_query(F.data == "alerts_90")
async def cb_alerts_90(cq: CallbackQuery):
    await send_alerts(cq.message, 90)
    await cq.answer()
