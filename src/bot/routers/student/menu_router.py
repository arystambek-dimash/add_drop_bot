from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

student_menu_router = Router()


@student_menu_router.callback_query(lambda c: c.data == "old_my_sdu_menu")
async def show_old_my_sdu_menu(callback: CallbackQuery, state: FSMContext):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Профиль", callback_data="profile"),
             InlineKeyboardButton(text="Транскрипт", callback_data="transcript")],
            [InlineKeyboardButton(text="Расписание", callback_data="schedule"),
             InlineKeyboardButton(text="Оценки", callback_data="grades")],
            [InlineKeyboardButton(text="Назад", callback_data="go_back_main_menu")]
        ]
    )

    await callback.message.edit_text(
        text="Меню портала old my sdu",
        reply_markup=inline_kb
    )
    await callback.answer()


@student_menu_router.callback_query(lambda c: c.data == "go_back_main_menu")
async def go_back_main_menu(callback: CallbackQuery, state: FSMContext):
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Портал", callback_data="old_my_sdu_menu"),
            ],
            [
                InlineKeyboardButton(text="Мои желаемые предметы", callback_data="wanted_subjects"),
            ],
            [
                InlineKeyboardButton(text="Выйти", callback_data="wanted_subjects"),
            ],
            [
                InlineKeyboardButton(text="О приложений", callback_data="about"),
            ]
        ]
    )
    await callback.message.edit_text(
        text="Главное меню",
        reply_markup=inline_kb
    )
    await callback.answer()
