"""
Модуль для настройки и запуска веб-приложения FastAPI.

Этот модуль инициализирует приложение FastAPI и включает маршруты для работы с пользователями
и задачами, определенные в отдельных модулях.

Основные компоненты:
- app: Экземпляр FastAPI, который обрабатывает HTTP-запросы.
- include_router: Используется для подключения маршрутов из модулей users и tasks.

Примечание:
- Убедитесь, что все необходимые маршруты и обработчики определены в соответствующих модулях.
- Для запуска приложения используйте команду: `uvicorn имя_файла:app --reload`.
"""


from fastapi import FastAPI
from .endpoints import users
from .endpoints import tasks

app = FastAPI(
    title="Task Manager API",  # Название API
    description="API для управления задачами пользователей",  # Описание API
    version="1.0.0",  # Версия API
)
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
@app.get("/", tags=["root"])
def read_root():
    """
    Корневой маршрут для проверки работоспособности API.

    Возвращает:
        dict: Сообщение с приветствием.
    """
    return {"message": "Welcome to the Task Manager API"}
