import json

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Callable, Dict, Any, Awaitable

from sqlalchemy.util import await_only

from src.adapters.parser.login_service import login_and_save_cookies
from src.domain.interfaces.redis_repository_interface import IRedisRepository
from src.domain.interfaces.student_repository_interface import IStudentRepository


class RedisSessionMiddleware(BaseMiddleware):
    def __init__(self, redis_repository: IRedisRepository, student_repository: IStudentRepository):
        super().__init__()
        self.redis_repository = redis_repository
        self.student_repository = student_repository

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        user_id = event.from_user.id
        session_data = await self.redis_repository.get(str(user_id))
        if session_data is None:
            student = await self.student_repository.get_by_telegram_id(str(user_id))
            if student is not None:
                cookies = await login_and_save_cookies(student.student_id, student.student_password)
                await self.redis_repository.set(str(user_id), json.dumps(cookies), expire=3600)
        print(session_data)
        return await handler(event, data)
