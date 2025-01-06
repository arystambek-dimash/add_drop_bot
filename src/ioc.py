from dependency_injector import containers, providers

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from src.adapters.database.redis import redis_connection
from src.adapters.repositories.redis_repository import RedisRepository
from src.adapters.repositories.student_repository import StudentRepository
from src.config import get_settings
from src.adapters.database.postgres import get_engine, create_session

from src.domain.interfaces.student_repository_interface import IStudentRepository


class AppContainer(containers.DeclarativeContainer):
    config = providers.Singleton(get_settings)

    bot = providers.Singleton(
        Bot,
        token=config.provided.TELEGRAM_TOKEN
    )
    storage = providers.Singleton(MemoryStorage)

    dispatcher = providers.Singleton(
        Dispatcher,
        storage=storage,

    )

    engine = providers.Singleton(
        get_engine,
        settings=config
    )

    session_maker = providers.Singleton(
        create_session,
        engine=engine
    )

    session = providers.Resource(
        lambda session_maker: session_maker(),
        session_maker=session_maker
    )

    redis_connection_provider = providers.Resource(
        redis_connection, settings=config
    )

    redis_repository = providers.Factory(
        RedisRepository, redis=redis_connection_provider
    )

    student_repository: providers.Factory[IStudentRepository] = providers.Factory(
        StudentRepository,
        session=session
    )
