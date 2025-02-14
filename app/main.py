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

app = FastAPI()
app.include_router(users.router)
app.include_router(tasks.router)
