"""
Модуль для управления миграциями базы данных с использованием Alembic и SQLAlchemy.

Этот модуль настраивает и запускает миграции для базы данных, используя асинхронный движок SQLAlchemy.

Импортируемые модули:
- alembic.context: Предоставляет контекст для выполнения миграций.
- sqlalchemy.ext.asyncio: Для создания асинхронного движка подключения к базе данных.
- sqlalchemy.future: Для работы с будущими версиями SQLAlchemy.
- logging.config: Для настройки логгирования.
- asyncio: Для работы с асинхронным программированием.

Импортируемые модели:
- Base: Основная модель, содержащая метаданные для всех моделей приложения.

Функции:
- run_migrations_online: Настраивает и запускает асинхронные миграции.
- run_async_migrations: Асинхронная функция, которая выполняет миграции в контексте подключения.
- do_run_migrations: Конфигурирует контекст миграции и выполняет миграции в рамках транзакции.

Примечания:
- Убедитесь, что URL подключения к базе данных указан в конфигурации Alembic.
- Этот модуль должен быть запущен в асинхронной среде для корректной работы.
"""

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.future import Connection
from logging.config import fileConfig
import asyncio

# Импортируем ваши модели
from app.models import Base

# Настройка логгирования
config = context.config
fileConfig(config.config_file_name)

# Указываем метаданные для Alembic
target_metadata = Base.metadata

def run_migrations_online():
    """
    Создает асинхронный движок подключения и запускает миграции.

    Эта функция настраивает асинхронный движок SQLAlchemy и запускает миграции,
    используя асинхронный контекст подключения.
    """
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        echo=True,
    )

    async def run_async_migrations():
        """
        Асинхронная функция для выполнения миграций.

        Эта функция устанавливает соединение с базой данных и запускает
        миграции с помощью функции do_run_migrations.
        """
        async with connectable.connect() as connection:
            # Начинаем транзакцию
            await connection.run_sync(do_run_migrations)

    # Запускаем асинхронные миграции
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_async_migrations())

def do_run_migrations(connection: Connection):
    """
    Конфигурирует и выполняет миграции.

    :param connection: Объект подключения к базе данных.
    Эта функция настраивает контекст миграции и выполняет миграции в рамках транзакции.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

run_migrations_online()
