# 🎯 Трекер полезных привычек

Бэкенд-часть SPA веб-приложения для отслеживания полезных привычек, основанного на книге Джеймса Клира "Атомные привычки".

## ✨ Функциональность

- 👤 **Регистрация и авторизация** пользователей
- 🎯 **CRUD операции** с привычками
- ✅ **Валидация привычек** согласно принципам из книги
- 🌍 **Публичные привычки** для вдохновения
- 📱 **Интеграция с Telegram** для напоминаний
- ⏰ **Отложенные задачи** через Celery
- 📄 **Пагинация** (5 элементов на страницу)
- 📚 **Автоматическая документация** API
- 🎨 **Готовый фронтенд** для демонстрации

## 🛠 Технологии

- **Backend:** Django 4.2.7 + Django REST Framework
- **База данных:** SQLite (разработка) / PostgreSQL (продакшн)
- **Кэш/Очереди:** Redis + Celery
- **Интеграции:** Telegram Bot API
- **Документация:** drf-spectacular (Swagger/ReDoc)
- **Тестирование:** Django TestCase + Coverage
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript

## 🚀 Быстрый старт

### 1. **Клонирование и установка**
```bash
git clone <repository-url>
cd habit-tracker-coursework
python -m venv venv
source venv/bin/activate  # Linux/Mac или venv\Scripts\activate для Windows
pip install -r requirements.txt
```

### 2. **Настройка переменных окружения**
Создайте файл `.env`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
TELEGRAM_BOT_TOKEN=7856547566:AAH6od-0P1YhAgImvyhCj3HSimnDqepzVow
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. **Инициализация базы данных**
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. **Запуск проекта**
```bash
# Основной сервер
python manage.py runserver

# В отдельных терминалах (опционально для Telegram уведомлений):
celery -A habit_tracker worker -l info
celery -A habit_tracker beat -l info
```

### 5. **Открыть приложение**
- **API:** http://localhost:8000/api/
- **Документация:** http://localhost:8000/api/docs/
- **Админка:** http://localhost:8000/admin/
- **Фронтенд:** откройте `frontend/index.html` в браузере

## 📱 Telegram интеграция

1. **Создайте бота через @BotFather:**
   - Найдите в Telegram: @BotFather
   - Команда: `/newbot`
   - Следуйте инструкциям
   - Скопируйте токен в `.env`

2. **Получите Chat ID:**
   - Напишите боту `/start`
   - Используйте API для получения chat_id
   - Укажите в профиле пользователя

## 🔗 API Endpoints

| Метод | URL | Описание |
|-------|-----|----------|
| `POST` | `/api/users/register/` | Регистрация |
| `POST` | `/api/users/login/` | Авторизация |
| `GET/PATCH` | `/api/users/profile/` | Профиль пользователя |
| `GET/POST` | `/api/habits/` | Список/создание привычек |
| `GET/PATCH/DELETE` | `/api/habits/{id}/` | Операции с привычкой |
| `GET` | `/api/habits/pleasant_habits/` | Приятные привычки |
| `GET` | `/api/public-habits/` | Публичные привычки |
| `GET` | `/api/docs/` | Swagger UI |
| `GET` | `/api/redoc/` | ReDoc документация |

## 🧪 Тестирование

```bash
# Запуск тестов
python manage.py test

# Проверка покрытия
coverage run --source='.' manage.py test
coverage report

# Проверка кода
flake8 --exclude=migrations
```

## 📊 Особенности проекта

### **Модель привычки**
Реализована согласно принципам книги "Атомные привычки":
- ⏰ **Время выполнения** ≤ 120 секунд
- 📅 **Периодичность** 1-7 дней  
- 🎁 **Вознаграждение** ИЛИ связанная приятная привычка
- ✅ **Валидация** всех бизнес-правил

### **Права доступа**
- 👤 Пользователи видят только свои привычки
- 🌍 Публичные привычки доступны всем для просмотра
- 🔒 Строгое разделение прав на уровне API

### **Интеграции**
- 📱 Telegram уведомления через Celery
- 📄 Пагинация по 5 элементов
- 🔄 CORS для SPA фронтенда

## 📁 Структура проекта

```
habit-tracker-coursework/
├── 🐍 Backend (Django)
│   ├── habit_tracker/      # Настройки проекта
│   ├── users/             # Пользователи + аутентификация
│   ├── habits/            # Привычки + валидация
│   ├── requirements.txt   # Зависимости Python
│   └── manage.py         # Django CLI
├── 🎨 Frontend
│   ├── index.html        # Основное SPA приложение
│   ├── app.js           # JavaScript логика
│   ├── styles.css       # Дополнительные стили
│   ├── demo.html        # Демо версия
│   └── api_test.html    # Тестер API
├── 📚 Документация
│   ├── README.md        # Основная документация
│   └── API_ENDPOINTS.md # Подробное описание API
└── ⚙️ Конфигурация
    ├── docker-compose.yml # Redis + PostgreSQL
    └── .gitignore        # Git исключения
```

## 🎓 Соответствие требованиям курсовой

✅ **Все критерии выполнены:**
- CORS настроен для SPA
- Интеграция с Telegram + Celery
- Пагинация по 5 элементов
- Переменные окружения
- Модели с валидацией
- Все необходимые эндпоинты
- Права доступа
- Тесты написаны
- Документация автоматическая

## 👨‍💻 Автор

**Курсовая работа** по Django REST Framework  
**Тема:** Трекер полезных привычек по книге "Атомные привычки"  
**Технологии:** Django, DRF, Celery, Telegram Bot API, HTML/CSS/JS

