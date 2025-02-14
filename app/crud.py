"""
Модуль для работы с пользователями и задачами в асинхронном веб-приложении.

Этот модуль предоставляет функции для создания и получения информации о пользователях и их задачах
в базе данных с использованием асинхронной сессии SQLAlchemy.

Основные функции:
- get_user: Получает пользователя по его идентификатору.
- create_user: Создает нового пользователя в базе данных.
- get_tasks: Получает список задач для указанного пользователя.
- create_user_task: Создает новую задачу для указанного пользователя.

Зависимости:
- sqlalchemy.ext.asyncio.AsyncSession: Для асинхронного взаимодействия с базой данных.
- .models: Модуль, содержащий определения моделей базы данных.
- .schemas: Модуль, содержащий схемы валидации данных с использованием Pydantic.

Примечание:
- Все функции используют асинхронные подходы для повышения производительности и масштабируемости.
"""


from sqlalchemy.ext.asyncio import AsyncSession
from . import models, schemas

async def get_user(db: AsyncSession, user_id: int):
    """
    Получает пользователя по его ID.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        user_id (int): ID пользователя.

    Returns:
        models.User: Объект пользователя, если найден, иначе None.
    """
    return await db.get(models.User, user_id)

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    """
    Создает нового пользователя.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        user (schemas.UserCreate): Данные для создания пользователя.

    Returns:
        models.User: Созданный объект пользователя.
    """
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_tasks(db: AsyncSession, user_id: int):
    """
    Получает список задач для конкретного пользователя.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        user_id (int): ID пользователя.

    Returns:
        List[models.Task]: Список задач пользователя.
    """
    user = await db.get(models.User, user_id)
    return user.tasks

async def create_user_task(db: AsyncSession, task: schemas.TaskCreate, user_id: int):
    """
    Создает новую задачу для пользователя.

    Args:
        db (AsyncSession): Асинхронная сессия SQLAlchemy.
        task (schemas.TaskCreate): Данные для создания задачи.
        user_id (int): ID пользователя, для которого создается задача.

    Returns:
        models.Task: Созданный объект задачи.
    """
    db_task = models.Task(**task.dict(), user_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task