from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from tg_bot_dev.services import Parser
from tg_bot_dev.utils import get_main_menu, get_acl_message, add_user_in_acl, del_user_from_acl
from tg_bot_dev.states import AddUserState, DelUserState

router = Router()


@router.message(F.text==("Добавить пользователя"))
async def add_user(message: Message, state: FSMContext):
    await message.answer("Введите id пользователя, которого вы хотите добавить")
    await state.set_state(AddUserState.waiting_for_id) 

@router.message(F.text==("Удалить пользователя"))
async def del_user(message: Message, state: FSMContext):
    await message.answer("Введите id пользователя, которого вы хотите удалить")
    await state.set_state(DelUserState.waiting_for_id) 

 
@router.message(F.text==("Текущий список пользователей"))
async def list_user(message: Message):
    menu = get_main_menu(message)
    if menu:
        ans = get_acl_message()
        await message.answer(ans, reply_keyboard=menu)
    return

@router.message(AddUserState.waiting_for_id)
async def process_add_user(message: Message, state: FSMContext):
    text = message.text.strip()
    menu = get_main_menu(message)
    if text in ("Основное меню"):
        await message.answer("Добавление отменено", reply_keyboard=menu)
        await state.clear()
        return

    if not text.isdigit():
        await message.answer("ID должен быть числом. Попробуйте снова или напишите \n```Основное меню```.")
        return
    user_id = int(text)
    add_user_in_acl(user_id)
    acl = get_acl_message()
    ans = "Успешно, обновленный acl:  \n" +acl
    if menu:
        await message.answer(ans, reply_keyboard=menu)
    return

@router.message(DelUserState.waiting_for_id)
async def process_del_user(message: Message, state: FSMContext):
    text = message.text.strip()
    menu = get_main_menu(message)
    if text in ("Основное меню"):
        await message.answer("Удаление отменено", reply_keyboard=menu)
        await state.clear()
        return

    if not text.isdigit():
        await message.answer("ID должен быть числом. Попробуйте снова или напишите \n```Основное меню```.")
        return
    user_id = int(text)
    del_user_from_acl(user_id)
    acl = get_acl_message()
    ans = "Успешно, обновленный acl:  \n" +acl
    if menu:
        await message.answer(ans, reply_keyboard=menu)
    return

