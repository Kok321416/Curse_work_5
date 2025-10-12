#!/bin/bash

# Скрипт для деплоя на сервер
set -e

echo "🚀 Начинаем деплой Habit Tracker..."

# Проверка переменных окружения
if [ -z "$HOST" ] || [ -z "$USERNAME" ]; then
    echo "❌ Ошибка: Установите переменные HOST и USERNAME"
    exit 1
fi

# Функция для выполнения команд на сервере
run_remote() {
    ssh -o StrictHostKeyChecking=no $USERNAME@$HOST "$1"
}

# Обновление кода на сервере
echo "📦 Обновление кода..."
run_remote "cd /opt/habit_tracker && git pull origin main"

# Остановка старых контейнеров
echo "🛑 Остановка старых контейнеров..."
run_remote "cd /opt/habit_tracker && docker-compose -f docker-compose.prod.yml down"

# Сборка новых образов
echo "🔨 Сборка новых образов..."
run_remote "cd /opt/habit_tracker && docker-compose -f docker-compose.prod.yml build --no-cache"

# Запуск контейнеров
echo "▶️ Запуск контейнеров..."
run_remote "cd /opt/habit_tracker && docker-compose -f docker-compose.prod.yml up -d"

# Ожидание запуска
echo "⏳ Ожидание запуска сервисов..."
sleep 30

# Применение миграций
echo "🗄️ Применение миграций..."
run_remote "cd /opt/habit_tracker && docker-compose -f docker-compose.prod.yml exec -T web python manage.py migrate"

# Сбор статических файлов
echo "📁 Сбор статических файлов..."
run_remote "cd /opt/habit_tracker && docker-compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput"

# Проверка здоровья
echo "🏥 Проверка здоровья сервисов..."
run_remote "cd /opt/habit_tracker && docker-compose -f docker-compose.prod.yml ps"

# Очистка
echo "🧹 Очистка неиспользуемых образов..."
run_remote "docker system prune -f"

echo "✅ Деплой завершен успешно!"
echo "🌐 Приложение доступно по адресу: http://$HOST"
