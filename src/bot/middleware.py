import json
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from src.adapters.parser.login_service import login_and_save_cookies
from src.bot.handlers.start_menu_handler import start_menu_handler
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository


class RedisSessionMiddleware(BaseMiddleware):
    def __init__(self, redis_repository: IRedisRepository, student_repository: IStudentRepository):
        super().__init__()
        self.redis_repository = redis_repository
        self.student_repository = student_repository

    async def handle_expired_session(self, event: Message | CallbackQuery):
        message = "Ваш(-а) сессия истекла, пожалуйста авторизуйтесь заново."
        if isinstance(event, CallbackQuery):
            await event.answer(message, show_alert=True)
            await start_menu_handler(event.message, False)
        else:
            await event.answer(message)
            await start_menu_handler(event, False)

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = str(event.from_user.id)
        session_data = await self.redis_repository.get(user_id)
        if session_data is None:
            student = await self.student_repository.get_by_telegram_id(user_id)
            if student is not None and student.is_active:
                cookies = await login_and_save_cookies(
                    student.student_id,
                    student.student_password
                )
                await self.redis_repository.set(
                    user_id,
                    json.dumps(cookies),
                    expire=3600
                )
            else:
                await self.handle_expired_session(event)
                return
        return await handler(event, data)
