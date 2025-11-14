from aiogram.fsm.state import State, StatesGroup

class DelUserState(StatesGroup):
    waiting_for_id = State()
