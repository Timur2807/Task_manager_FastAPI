"""
Модуль маршрутов для управления задачами пользователей.
Этот модуль содержит маршруты API для создания и получения задач, связанных с пользователями.
Использует FastAPI для обработки HTTP-запросов и SQLAlchemy для работы с асинхронной базой данных.
Основные функции:
- Создание задачи для указанного пользователя.
- Получение всех задач для указанного пользователя.
Зависимости:
- FastAPI: для создания API.
- SQLAlchemy: для работы с асинхронной базой данных.
- Pydantic: для валидации и сериализации данных.
Модуль также использует CRUD-операции, определенные в другом модуле, для взаимодействия с базой данных.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import schemas, crud
from ..database import AsyncSessionLocal

router = APIRouter()


async def get_db() -> AsyncSession:
    """
    Получает экземпляр асинхронной сессии базы данных.

    Используется в качестве зависимости для маршрутов, чтобы обеспечить
    доступ к базе данных. Сессия закрывается после завершения запроса.

    Yields:
        AsyncSession: Асинхронная сессия базы данных.
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()


@router.post("/users/{user_id}/tasks/", response_model=schemas.Task)
async def create_task_for_user(
    user_id: int,
    task: schemas.TaskCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.Task:
    """
    Создает задачу для указанного пользователя.

    Args:
        user_id (int): Идентификатор пользователя, для которого создается задача.
        task (schemas.TaskCreate): Данные задачи для создания.
        db (AsyncSession): Сессия базы данных.

    Returns:
        schemas.Task: Созданная задача.

    Raises:
        HTTPException: Если пользователь не найден или возникает ошибка при создании задачи.
    """
    return await crud.create_user_task(db, task, user_id)


@router.get("/tasks/", response_model=list[schemas.Task])
async def read_tasks(user_id: int, db: AsyncSession = Depends(get_db)) -> list[schemas.Task]:
    """
    Читает все задачи для указанного пользователя.

    Args:
        user_id (int): Идентификатор пользователя, для которого нужно получить задачи.
        db (AsyncSession): Сессия базы данных.

    Returns:
        list[schemas.Task]: Список задач для указанного пользователя.

    Raises:
        HTTPException: Если пользователь не найден или возникает ошибка при получении задач.
    """
    return await crud.get_tasks(db, user_id)
