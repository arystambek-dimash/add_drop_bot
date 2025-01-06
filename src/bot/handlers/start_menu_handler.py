from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton


async def start_menu_handler(message: Message,
                             is_start: bool = True):
    greeting_text = (
        "Привет! Я бот, который поможет автоматически выбирать предметы в Old My SDU "
        "и обеспечит лёгкий доступ к платформе.\n\n"
        "Выбери один из вариантов:"
    )
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Авторизоваться", callback_data="auth")
            ],
            [
                InlineKeyboardButton(text="О приложении", callback_data="about")
            ]
        ]
    )
    if is_start:
        await message.answer(text=greeting_text, reply_markup=inline_kb)
    else:
        await message.edit_text(text=greeting_text, reply_markup=inline_kb)
