from aiogram.fsm.state import StatesGroup, State


class StudentLoginState(StatesGroup):
    CHOICE = State()
    WAITING_FOR_STUDENT_ID = State()
    WAITING_FOR_PASSWORD = State()


class UserState(StatesGroup):
    user_id = State()
