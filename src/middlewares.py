from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery


class UserIDMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if isinstance(event, (Message, CallbackQuery)):
            state = data.get('state')
            if state:
                await state.update_data(user_id=str(event.from_user.id))
        return await handler(event, data)
