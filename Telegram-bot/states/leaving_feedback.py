from aiogram.fsm.state import StatesGroup, State


class LeaveFeedback(StatesGroup):
    user_id = ""
    chat_id = ""
    username = ""
    email = State()
    comment = State()
