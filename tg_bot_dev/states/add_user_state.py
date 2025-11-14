from aiogram.fsm.state import State, StatesGroup

class AddUserState(StatesGroup):
    waiting_for_id = State()
