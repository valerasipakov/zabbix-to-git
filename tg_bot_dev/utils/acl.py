from tg_bot_dev.keyboards import main_menu, main_menu_admin, admin_menu
from aiogram.types import Message
from tg_bot_dev.settings import settings


# --- Хелпер: проверка ACL ---
def is_user(msg: Message) -> bool:
    print(settings.acl_ids, f'Get message from {msg.from_user.id} is it in acl: {msg.from_user.id in settings.acl_ids}')
    uid = msg.from_user.id if msg.from_user else None
    return uid in settings.acl_ids


# --- Хелпер: проверка ACL ---
def is_admin(msg: Message) -> bool:
    print(settings.acl_ids, f'Get message from {msg.from_user.id}is it in admin list: {msg.from_user.id in settings.admins_ids}')
    uid = msg.from_user.id if msg.from_user else None
    return uid in settings.admins_ids

# --- Определяем меню в зависимости от пользователя ---
def get_main_menu(msg: Message):
    if is_admin(msg):
        return main_menu_admin
    if is_user(msg):
        return main_menu
    return None

# --- Управляет доступом в админ зону
def get_admin_zone_menu(msg: Message):
    print(settings.acl_ids, f'Get admin-zone requere from {msg.from_user.id}is it in admin list: {msg.from_user.id in settings.admins_ids}')
    if is_admin(msg):
        return admin_menu
    return None

def get_acl_message():
    message = "Users:\n"
    for user in settings.acl_ids:
        message = message + str(user) + "\n"
    message = message + "Admins: \n"
    for admin in settings.admins_ids:
        message = message + str(admin) + "\n"
    return message


def add_user_in_acl(id: int):
    settings.acl_ids.add(id)

def del_user_from_acl(id: int):
    settings.acl_ids.remove(id)
