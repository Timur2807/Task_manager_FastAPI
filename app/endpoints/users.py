"""
Этот модуль предоставляет маршруты для создания и получения информации о пользователях.
Основные функции:
- Создание нового пользователя через POST-запрос на /users/.
- Получение информации о пользователе по его идентификатору через GET-запрос на /users/{user_id}.

Зависимости:
- FastAPI: для обработки HTTP-запросов и маршрутизации.
- SQLAlchemy: для асинхронного взаимодействия с базой данных.
- Pydantic: для валидации и сериализации данных.

Использует:
- CRUD-операции, определенные в другом модуле, для взаимодействия с базой данных.
- Асинхронные сессии для управления подключениями к базе данных.

Примечание:
- Все маршруты используют асинхронные функции для повышения производительности.
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
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

@router.post("/users/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(get_db)
) -> schemas.User:
    """
    Создает нового пользователя.

    Args:
        user (schemas.UserCreate): Данные нового пользователя, которые нужно создать.
        db (AsyncSession): Сессия базы данных.

    Returns:
        schemas.User: Созданный пользователь.

    Raises:
        HTTPException: Если возникает ошибка при создании пользователя.
    """
    return await crud.create_user(db, user)

@router.get("/users/{user_id}", response_model=schemas.User)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> schemas.User:
    """
    Получает информацию о пользователе по его идентификатору.

    Args:
        user_id (int): Идентификатор пользователя, информацию о котором нужно получить.
        db (AsyncSession): Сессия базы данных.

    Returns:
        schemas.User: Информация о пользователе.

    Raises:
        HTTPException: Если пользователь с указанным идентификатором не найден.
    """
    db_user = await crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
