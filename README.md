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

- **Backend:** Django 4.2.7 + Django REST Framework
- **База данных:** PostgreSQL 15
- **Кэш/Очереди:** Redis 7 + Celery
- **Интеграции:** Telegram Bot API
- **Контейнеризация:** Docker + Docker Compose
- **Документация:** drf-spectacular (Swagger/ReDoc)

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

Создайте файл `.env` на основе шаблона:

```bash
# Скопировать шаблон
cp env_template .env

# Отредактировать файл .env и указать:
# - SECRET_KEY (для продакшн)
# - TELEGRAM_BOT_TOKEN (ваш токен бота)
# - Другие настройки при необходимости
```

### 5. Запуск через Docker (рекомендуемый способ)

```bash
# Запустить все сервисы (PostgreSQL, Redis, Django, Celery)
docker-compose up -d

# Создать суперпользователя
docker-compose exec web python manage.py createsuperuser

# Проверить статус сервисов
docker-compose ps
```

**Доступные сервисы:**
- **API:** http://localhost:8000/api/
- **Документация:** http://localhost:8000/api/docs/
- **Админка:** http://localhost:8000/admin/

### Альтернативный запуск (без Docker)

```bash
# Запуск зависимостей
docker-compose up -d db redis

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Запуск сервера разработки
python manage.py runserver

# В отдельных терминалах:
celery -A habit_tracker worker -l info
celery -A habit_tracker beat -l info
```

## Проверка работоспособности сервисов

После запуска `docker-compose up -d` проверьте статус всех сервисов:

```bash
# Проверить статус контейнеров
docker-compose ps

# Проверить логи
docker-compose logs web
docker-compose logs celery
docker-compose logs celery-beat

# Проверить подключение к базе данных
docker-compose exec db psql -U postgres -d habit_tracker -c "SELECT 1;"

# Проверить Redis
docker-compose exec redis redis-cli ping

# Проверить Django приложение
curl http://localhost:8000/api/docs/
```

**Ожидаемые результаты:**
- **Web сервис:** http://localhost:8000/api/docs/ открывается
- **База данных:** команда возвращает "1"
- **Redis:** команда возвращает "PONG"
- **Celery:** в логах нет ошибок подключения

## Создание Telegram бота

1. Найдите в Telegram бота @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в файл `.env`

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
├── 🐳 Docker
│   ├── Dockerfile              # Образ Django приложения
│   ├── docker-compose.yml      # Оркестрация сервисов
│   ├── .dockerignore          # Исключения для Docker
│   └── env_template           # Шаблон переменных окружения
├── 🐍 Backend
│   ├── habit_tracker/         # Настройки Django проекта
│   ├── users/                 # Пользователи и аутентификация
│   ├── habits/                # Привычки и валидация
│   ├── manage.py             # Django CLI
│   └── requirements.txt      # Python зависимости
├── 🎨 Frontend
│   ├── index.html            # SPA приложение
│   ├── app.js               # JavaScript логика
│   ├── styles.css           # Стили
│   └── api_test.html        # Тестер API
└── 📚 Документация
    ├── README.md            # Основная документация
    └── API_ENDPOINTS.md     # Описание API
```

## Docker сервисы

Проект включает следующие контейнеры:

| Сервис | Описание | Порт | Зависимости |
|--------|----------|------|-------------|
| **web** | Django приложение | 8000 | db, redis |
| **db** | PostgreSQL база данных | 5432 | - |
| **redis** | Redis для Celery | 6379 | - |
| **celery** | Celery worker | - | db, redis |
| **celery-beat** | Планировщик задач | - | db, redis |
