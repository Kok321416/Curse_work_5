# 🚀 Полезные команды

## Docker команды

### Основные операции
```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка всех сервисов
docker-compose down

# Перезапуск сервисов
docker-compose restart

# Просмотр статуса
docker-compose ps

# Просмотр логов
docker-compose logs -f web
docker-compose logs -f celery
```

### Работа с Django
```bash
# Выполнение команд Django
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic

# Запуск тестов
docker-compose exec web python manage.py test

# Доступ к shell Django
docker-compose exec web python manage.py shell

# Доступ к bash контейнера
docker-compose exec web bash
```

### Работа с базой данных
```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U postgres -d habit_tracker

# Создание дампа БД
docker-compose exec db pg_dump -U postgres habit_tracker > backup.sql

# Восстановление из дампа
docker-compose exec -T db psql -U postgres -d habit_tracker < backup.sql
```

### Работа с Redis
```bash
# Подключение к Redis CLI
docker-compose exec redis redis-cli

# Очистка Redis
docker-compose exec redis redis-cli FLUSHALL

# Мониторинг Redis
docker-compose exec redis redis-cli MONITOR
```

## Разработка

### Локальная разработка
```bash
# Запуск только БД и Redis
docker-compose up -d db redis

# Локальный запуск Django
python manage.py runserver

# Локальный запуск Celery
celery -A habit_tracker worker -l info
celery -A habit_tracker beat -l info
```

### Тестирование
```bash
# Запуск всех тестов
python manage.py test

# Запуск тестов с покрытием
coverage run --source='.' manage.py test
coverage report
coverage html

# Проверка кода
flake8 --exclude=migrations
```

## Отладка

### Просмотр логов
```bash
# Логи всех сервисов
docker-compose logs

# Логи конкретного сервиса
docker-compose logs web
docker-compose logs celery
docker-compose logs db

# Следить за логами в реальном времени
docker-compose logs -f web
```

### Проверка состояния
```bash
# Статус контейнеров
docker-compose ps

# Использование ресурсов
docker stats

# Проверка сетей
docker network ls
docker-compose exec web ping db
```

## Очистка

### Очистка Docker
```bash
# Остановка и удаление контейнеров
docker-compose down

# Удаление с volumes
docker-compose down -v

# Очистка неиспользуемых образов
docker system prune

# Полная очистка
docker system prune -a --volumes
```

## Продакшн

### Сборка для продакшн
```bash
# Сборка образов
docker-compose build

# Запуск в продакшн режиме
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Обновление без даунтайма
docker-compose up -d --no-deps web
```
