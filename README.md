# Трекер полезных привычек

Бэкенд-часть SPA веб-приложения для отслеживания полезных привычек, основанного на книге Джеймса Клира "Атомные привычки".

## Функциональность

- Регистрация и авторизация пользователей
- CRUD операции с привычками
- Валидация привычек согласно принципам из книги
- Публичные привычки для вдохновения
- Интеграция с Telegram для напоминаний
- Отложенные задачи через Celery
- Пагинация (5 элементов на страницу)
- Автоматическая документация API

## Технологии

- Django 4.2.7
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Telegram Bot API
- Docker

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd Curse_work_5
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env` на основе `env_example.txt`:

```bash
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/habit_tracker
REDIS_URL=redis://localhost:6379/0
TELEGRAM_BOT_TOKEN=your-telegram-bot-token-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Запуск зависимостей (PostgreSQL и Redis)

```bash
docker-compose up -d
```

### 6. Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Создание суперпользователя

```bash
python manage.py createsuperuser
```

### 8. Запуск сервера разработки

```bash
python manage.py runserver
```

### 9. Запуск Celery worker (в отдельном терминале)

```bash
celery -A habit_tracker worker -l info
```

### 10. Запуск Celery beat (в отдельном терминале)

```bash
celery -A habit_tracker beat -l info
```

## Создание Telegram бота

1. Найдите в Telegram бота @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в переменную окружения `TELEGRAM_BOT_TOKEN`

## API Endpoints

### Аутентификация
- `POST /api/users/register/` - Регистрация
- `POST /api/users/login/` - Авторизация
- `GET/PATCH /api/users/profile/` - Профиль пользователя

### Привычки
- `GET /api/habits/` - Список привычек пользователя
- `POST /api/habits/` - Создание привычки
- `GET /api/habits/{id}/` - Детали привычки
- `PATCH /api/habits/{id}/` - Обновление привычки
- `DELETE /api/habits/{id}/` - Удаление привычки
- `GET /api/habits/pleasant_habits/` - Список приятных привычек

### Публичные привычки
- `GET /api/public-habits/` - Список публичных привычек

### Документация
- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc
- `GET /api/schema/` - OpenAPI схема

## Тестирование

Запуск тестов:

```bash
python manage.py test
```

Проверка покрытия тестами:

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Проверка кода

```bash
flake8 --exclude=migrations
```

## Планирование напоминаний

Для планирования напоминаний о привычках:

```bash
python manage.py schedule_reminders
```

## Модель привычки

Привычка содержит следующие поля:
- `user` - пользователь-создатель
- `place` - место выполнения
- `time` - время выполнения
- `action` - действие
- `is_pleasant` - признак приятной привычки
- `related_habit` - связанная привычка (только приятная)
- `periodicity` - периодичность в днях (1-7)
- `reward` - вознаграждение
- `execution_time` - время выполнения в секундах (≤120)
- `is_public` - признак публичности

## Валидация

- Нельзя одновременно указывать вознаграждение и связанную привычку
- Время выполнения не более 120 секунд
- В связанные привычки попадают только приятные привычки
- У приятной привычки нет вознаграждения или связанной привычки
- Периодичность от 1 до 7 дней

## Права доступа

- Пользователи видят только свои привычки
- Публичные привычки доступны всем для просмотра
- Редактирование и удаление только своих привычек

## Структура проекта

```
habit_tracker/
├── habit_tracker/          # Основные настройки проекта
├── users/                  # Приложение пользователей
├── habits/                 # Приложение привычек
├── requirements.txt        # Зависимости
├── docker-compose.yml      # Docker конфигурация
└── README.md              # Документация
```
