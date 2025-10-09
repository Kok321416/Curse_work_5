FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Копирование и настройка entrypoint скрипта
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Создание директорий для статических файлов и медиа
RUN mkdir -p /app/staticfiles /app/media

# Создание пользователя для безопасности
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app && \
    chown appuser:appuser /entrypoint.sh

# Переключаемся на пользователя appuser
USER appuser

# Открытие порта
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/docs/ || exit 1

# Entrypoint и команда по умолчанию
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "habit_tracker.wsgi:application"]
