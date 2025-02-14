"""
Модуль для настройки асинхронного взаимодействия с базой данных в приложении Task Manager.

Этот модуль устанавливает соединение с базой данных PostgreSQL с использованием SQLAlchemy
и предоставляет необходимые компоненты для работы с асинхронными сессиями.

Основные компоненты:
- DATABASE_URL: URL для подключения к базе данных PostgreSQL.
- engine: Асинхронный движок SQLAlchemy для выполнения операций с базой данных.
- AsyncSessionLocal: Фабрика сессий для создания асинхронных сессий работы с базой данных.
- Base: Базовый класс для определения моделей базы данных с использованием SQLAlchemy.

Примечание:
- Убедитесь, что база данных доступна и параметры подключения указаны правильно.
- Движок настроен на вывод логов SQL-запросов для отладки (echo=True).
"""


from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:123@localhost:5432/task_manager_db"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

