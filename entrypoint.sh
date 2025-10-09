#!/bin/bash

# Ожидание готовности базы данных (если используется PostgreSQL)
if [ "$DATABASE_URL" ] && [[ "$DATABASE_URL" == *"postgresql"* ]]; then
    echo "Waiting for PostgreSQL database..."
    # Извлекаем хост и порт из DATABASE_URL
    DB_HOST=$(echo $DATABASE_URL | sed -n 's/.*@\([^:]*\):.*/\1/p')
    DB_PORT=$(echo $DATABASE_URL | sed -n 's/.*:\([0-9]*\)\/.*/\1/p')
    
    if [ "$DB_HOST" ] && [ "$DB_PORT" ]; then
        while ! nc -z $DB_HOST $DB_PORT; do
            echo "Waiting for database connection..."
            sleep 1
        done
        echo "Database is ready!"
    fi
fi

# Применение миграций
echo "Applying database migrations..."
python manage.py migrate --noinput

# Сбор статических файлов (если нужно)
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

# Создание суперпользователя (если переменные заданы)
if [ "$DJANGO_SUPERUSER_EMAIL" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$DJANGO_SUPERUSER_EMAIL').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser created')
else:
    print('Superuser already exists')
"
fi

# Запуск приложения
echo "Starting application..."
exec "$@"
