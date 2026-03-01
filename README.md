# Task Manager API

Бэкенд для системы управления задачами (Task Manager)

## Стек технологий
- FastAPI
- SQLite3
- JWT (python-jose)
- SQLAlchemy
- Alembic
- Bcrypt (passlib)

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/VivienWuds/task-manager-api.git
cd task-manager-api
2. Создать виртуальное окружение
bash
python -m venv venv
source venv/Scripts/activate  # для Windows
3. Установить зависимости
bash
pip install -r requirements.txt
4. Создать базу данных
bash
python
>>> from app.database import engine
>>> from app.models import Base
>>> Base.metadata.create_all(bind=engine)
>>> exit()
5. Запустить сервер
bash
python run.py
6. Открыть документацию
text
http://127.0.0.1:8000/docs
API Эндпоинты
Аутентификация
POST /auth/register - регистрация пользователя

POST /auth/login - вход в систему (получение JWT)

POST /auth/logout - выход из системы

Проекты
GET /projects/ - список проектов пользователя

POST /projects/ - создать новый проект

GET /projects/{id} - детальная информация о проекте

Задачи
POST /projects/{project_id}/tasks/ - создать задачу

PATCH /tasks/{task_id} - обновить задачу

DELETE /tasks/{task_id} - удалить задачу

Структура проекта
text
task-manager-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── auth.py
│   ├── dependencies.py
│   └── routers/
│       ├── __init__.py
│       ├── auth.py
│       ├── projects.py
│       └── tasks.py
├── requirements.txt
├── run.py
└── README.md
Модели данных
User
id (int, PK)

email (str, unique)

password_hash (str)

username (str, unique)

created_at (datetime)

Project
id (int, PK)

name (str)

description (str, optional)

owner_id (int, FK)

created_at (datetime)

updated_at (datetime)

Task
id (int, PK)

title (str)

description (str, optional)

status (str): "todo", "in_progress", "done"

project_id (int, FK, ondelete="CASCADE")

assignee_id (int, FK, nullable)

created_at (datetime)

updated_at (datetime)
