# 🖥️ Настройка сервера для Habit Tracker

## 📋 Требования к серверу

- **ОС:** Ubuntu 20.04+ или CentOS 8+
- **RAM:** Минимум 2GB, рекомендуется 4GB
- **CPU:** Минимум 1 vCPU, рекомендуется 2 vCPU
- **Диск:** Минимум 20GB SSD
- **Сеть:** Публичный IP адрес

## 🚀 Пошаговая настройка

### 1. Подключение к серверу
```bash
ssh root@YOUR_SERVER_IP
# или
ssh ubuntu@YOUR_SERVER_IP
```

### 2. Обновление системы
```bash
sudo apt update && sudo apt upgrade -y
sudo reboot
```

### 3. Установка Docker
```bash
# Удаление старых версий
sudo apt remove docker docker-engine docker.io containerd runc

# Установка зависимостей
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Добавление GPG ключа Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавление репозитория
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Установка Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
```

### 4. Установка Docker Compose
```bash
# Скачивание последней версии
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Права на выполнение
sudo chmod +x /usr/local/bin/docker-compose

# Проверка установки
docker-compose --version
```

### 5. Настройка Git
```bash
sudo apt install -y git
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 6. Создание директории проекта
```bash
sudo mkdir -p /opt/habit_tracker
sudo chown $USER:$USER /opt/habit_tracker
cd /opt/habit_tracker
```

### 7. Клонирование проекта
```bash
git clone https://github.com/YOUR_USERNAME/habit-tracker.git .
```

### 8. Настройка переменных окружения
```bash
cp env_template .env
nano .env
```

**Обязательно измените следующие параметры:**
```bash
SECRET_KEY=your-50-character-secret-key-here-change-this
DEBUG=False
ALLOWED_HOSTS=YOUR_SERVER_IP,your-domain.com
POSTGRES_PASSWORD=your-secure-database-password
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
```

### 9. Настройка файрвола
```bash
# Установка UFW
sudo apt install -y ufw

# Базовые правила
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Разрешение SSH
sudo ufw allow ssh
sudo ufw allow 22

# Разрешение HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Включение файрвола
sudo ufw enable
```

### 10. Первый запуск
```bash
# Сборка и запуск контейнеров
docker-compose -f docker-compose.prod.yml up -d --build

# Применение миграций
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Создание суперпользователя
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

## 🔐 Настройка SSH для GitHub Actions

### 1. Генерация SSH ключа
```bash
ssh-keygen -t ed25519 -C "github-actions@your-domain.com" -f ~/.ssh/github_actions
```

### 2. Добавление публичного ключа в authorized_keys
```bash
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 3. Копирование приватного ключа
```bash
cat ~/.ssh/github_actions
```

**Скопируйте весь вывод и добавьте в GitHub Secrets как `SSH_PRIVATE_KEY`**

## 📊 Мониторинг и логи

### Просмотр логов
```bash
# Все сервисы
docker-compose -f docker-compose.prod.yml logs -f

# Конкретный сервис
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f nginx
docker-compose -f docker-compose.prod.yml logs -f celery
```

### Мониторинг ресурсов
```bash
# Статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# Использование ресурсов
docker stats

# Место на диске
df -h
```

### Перезапуск сервисов
```bash
# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Перезапуск конкретного сервиса
docker-compose -f docker-compose.prod.yml restart web
```

## 🛠️ Обслуживание

### Обновление проекта
```bash
cd /opt/habit_tracker
git pull origin main
docker-compose -f docker-compose.prod.yml up -d --build
```

### Резервное копирование базы данных
```bash
# Создание бэкапа
docker-compose -f docker-compose.prod.yml exec db pg_dump -U habit_user habit_tracker_prod > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление из бэкапа
docker-compose -f docker-compose.prod.yml exec -T db psql -U habit_user -d habit_tracker_prod < backup_file.sql
```

### Очистка системы
```bash
# Удаление неиспользуемых образов
docker system prune -f

# Удаление всех неиспользуемых данных
docker system prune -a -f
```

## 🚨 Устранение неполадок

### Проблемы с контейнерами
```bash
# Проверка статуса
docker-compose -f docker-compose.prod.yml ps

# Перезапуск проблемного контейнера
docker-compose -f docker-compose.prod.yml restart CONTAINER_NAME

# Пересборка образов
docker-compose -f docker-compose.prod.yml build --no-cache
```

### Проблемы с базой данных
```bash
# Подключение к базе данных
docker-compose -f docker-compose.prod.yml exec db psql -U habit_user -d habit_tracker_prod

# Проверка миграций
docker-compose -f docker-compose.prod.yml exec web python manage.py showmigrations
```

### Проблемы с SSL (если используется)
```bash
# Обновление сертификатов Let's Encrypt
sudo certbot renew
docker-compose -f docker-compose.prod.yml restart nginx
```
