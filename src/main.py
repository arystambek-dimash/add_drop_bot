import asyncio
from dependency_injector.wiring import inject, Provide

from src.adapters.database.postgres import init_db
from src.bot.register import register_routers
from src.ioc import AppContainer

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery


@inject
async def main(
        container: AppContainer = Provide[AppContainer],
):
    bot = container.bot()
    dp = container.dispatcher()
    middleware = container.user_id_middleware()
    dp.update.middleware(middleware)
    dp.message.middleware(middleware)
    engine = container.engine()
    asyncio.create_task(init_db(engine))
    register_routers(
        dp=dp,
        student_repository=container.student_repository(),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    container = AppContainer()
    container.wire(modules=[__name__])
    asyncio.run(main())
