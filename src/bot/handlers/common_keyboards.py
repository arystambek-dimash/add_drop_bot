from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_menu_keyboard():
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Портал", callback_data="old_my_sdu_menu"),
                InlineKeyboardButton(text="Мои желаемые предметы", callback_data="wanted_subjects"),
            ],
            [
                InlineKeyboardButton(text="Свободные кабинеты", callback_data="free_cabinets"),
                InlineKeyboardButton(text="О приложений", callback_data="about"),
            ],
            [
                InlineKeyboardButton(text="Выйти", callback_data="logout"),
            ],
        ]
    )

    return inline_kb