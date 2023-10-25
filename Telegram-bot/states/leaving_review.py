from aiogram.fsm.state import StatesGroup, State


class LeaveReview(StatesGroup):
    place_id = ""
    author_name = State()
    description = State()
    grade = State()
