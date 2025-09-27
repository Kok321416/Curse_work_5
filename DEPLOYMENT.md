# 🚀 Развертывание проекта

## Локальная разработка

### Быстрый старт
```bash
git clone <repository-url>
cd habit-tracker-coursework
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### С Telegram уведомлениями
```bash
# Дополнительно запустить Redis и Celery
docker-compose up -d redis
celery -A habit_tracker worker -l info
celery -A habit_tracker beat -l info
```

## Продакшн развертывание

### 1. Переменные окружения (.env)
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost:5432/habit_tracker
REDIS_URL=redis://localhost:6379/0
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. База данных
```bash
# PostgreSQL
pip install psycopg2-binary
python manage.py migrate
python manage.py collectstatic
```

### 3. Веб-сервер (Nginx + Gunicorn)
```bash
pip install gunicorn
gunicorn habit_tracker.wsgi:application --bind 0.0.0.0:8000
```

### 4. Celery (systemd)
```bash
# /etc/systemd/system/celery.service
celery -A habit_tracker worker --loglevel=info
celery -A habit_tracker beat --loglevel=info
```

## Docker развертывание

### Dockerfile (пример)
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "habit_tracker.wsgi:application"]
```

### docker-compose.yml (продакшн)
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
  
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: habit_tracker
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
  
  redis:
    image: redis:7-alpine
  
  celery:
    build: .
    command: celery -A habit_tracker worker -l info
    depends_on:
      - db
      - redis
```

## Проверка развертывания

### Тесты
```bash
python manage.py test
coverage run --source='.' manage.py test
coverage report
```

### Проверка API
- http://localhost:8000/api/docs/ - Swagger UI
- http://localhost:8000/api/redoc/ - ReDoc
- http://localhost:8000/admin/ - Django Admin

### Мониторинг
- Логи Django: `debug.log`
- Логи Celery: через systemd или Docker
- Метрики Redis: через redis-cli
