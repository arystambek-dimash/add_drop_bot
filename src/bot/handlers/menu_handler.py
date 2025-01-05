from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from src.domain.interfaces.student_repository_interface import IStudentRepository

async def menu_handler(message: Message, state: FSMContext, student_repository: IStudentRepository):
    telegram_id = str(message.from_user.id)
    user = await student_repository.get_by_telegram_id(telegram_id)

    if not user:
        await message.answer("Вы не авторизованы! Нажмите /start для входа.")
        return

    first_name = user.first_name
    last_name = user.last_name
    menu_text = f"👋 {first_name} {last_name}"

    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Портал", callback_data="old_my_sdu_menu"),
            ],
            [
                InlineKeyboardButton(text="Мои хотелки", callback_data="wanted_subjects"),
            ],
            [
                InlineKeyboardButton(text="О приложений", callback_data="about"),
            ]
        ]
    )
    await message.answer(menu_text, reply_markup=inline_kb)
    await state.clear()