"""
Модуль моделей для системы управления задачами.

В этом модуле определены модели данных для пользователей и задач, используемые в приложении.
Модели основаны на SQLAlchemy и включают связи между пользователями и их задачами.

Классы:
- User: Модель, представляющая пользователя в системе, с уникальным именем и адресом электронной почты.
- Task: Модель, представляющая задачу, связанная с пользователем, с заголовком, описанием и сроком выполнения.

Использование:
- Модуль импортируется в другие части приложения для взаимодействия с базой данных.
- Объекты классов User и Task могут быть созданы, изменены и удалены через SQLAlchemy ORM.

Примечание:
- Убедитесь, что база данных и таблицы инициализированы перед использованием моделей.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    """
    Модель пользователя в системе.

    Атрибуты:
    - id (int): Уникальный идентификатор пользователя.
    - username (str): Уникальное имя пользователя.
    - email (str): Уникальный адрес электронной почты пользователя.
    - tasks (list[Task]): Список задач, связанных с пользователем.

    Связи:
    - Связь с моделью Task через атрибут owner.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    tasks = relationship("Task", back_populates="user")


class Task(Base):
    """
    Модель задачи в системе.

    Атрибуты:
    - id (int): Уникальный идентификатор задачи.
    - title (str): Заголовок задачи.
    - description (str): Описание задачи.
    - due_date (datetime): Дата и время завершения задачи.
    - user_id (int): Идентификатор пользователя, которому принадлежит задача.
    - owner (User ): Связанный пользователь, которому принадлежит задача.

    Связи:
    - Связь с моделью User через атрибут owner.
    """
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    due_date = Column(DateTime(timezone=True))
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="tasks")
