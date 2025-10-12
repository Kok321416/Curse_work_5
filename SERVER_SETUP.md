ssh -l superego 158.160.202.67# 🖥️ Настройка чистой виртуальной машины Yandex Cloud

## 📋 Создание виртуальной машины в Yandex Cloud

### 1. Создание ВМ через веб-интерфейс
1. Войдите в [Yandex Cloud Console](https://console.cloud.yandex.ru/)
2. Выберите каталог или создайте новый
3. Нажмите **"Создать ресурс"** → **"Виртуальная машина"**

### 2. Настройки виртуальной машины
- **Имя:** `habit-tracker-server`
- **Зона доступности:** `ru-central1-a`
- **Операционная система:** Ubuntu 22.04 LTS
- **vCPU:** 2 (минимум для Docker)
- **RAM:** 4 ГБ (рекомендуется)
- **Диск:** 20 ГБ SSD
- **Сеть:** Создать новую или использовать default
- **Публичный IP:** Обязательно включить!

### 3. SSH ключи
- **Создайте SSH ключ** на своем компьютере:
```bash
ssh-keygen -t ed25519 -C "yandex-cloud-vm"
```
- **Скопируйте публичный ключ** и добавьте в настройки ВМ
- **Пользователь:** `ubuntu` (по умолчанию)

### 4. Создание ВМ
- Нажмите **"Создать ВМ"**
- Дождитесь создания (2-3 минуты)
- **Запишите публичный IP адрес!**

## 🔌 Первое подключение к серверу

### 1. Подключение по SSH
```bash
ssh ubuntu@YOUR_PUBLIC_IP
```

### 2. Первичная настройка системы
```bash
# Обновление пакетов
sudo apt update && sudo apt upgrade -y

# Установка базовых утилит
sudo apt install -y curl wget git nano htop unzip

# Настройка часового пояса
sudo timedatectl set-timezone Europe/Moscow

# Перезагрузка для применения обновлений
sudo reboot
```

**После перезагрузки снова подключитесь по SSH**

## 🐳 Установка Docker и Docker Compose

### 1. Установка Docker
```bash
# Удаление старых версий (если есть)
sudo apt remove -y docker docker-engine docker.io containerd runc

# Установка зависимостей
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Добавление официального GPG ключа Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Добавление репозитория Docker
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Обновление индекса пакетов и установка Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER

# Включение автозапуска Docker
sudo systemctl enable docker
sudo systemctl start docker

# Проверка установки
sudo docker --version
sudo docker run hello-world
```

### 2. Установка Docker Compose (standalone)
```bash
# Загрузка последней версии Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Права на выполнение
sudo chmod +x /usr/local/bin/docker-compose

# Создание символической ссылки
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Проверка установки
docker-compose --version
```

### 3. Перезагрузка для применения групп
```bash
# Выход из SSH сессии
exit

# Повторное подключение
ssh ubuntu@YOUR_PUBLIC_IP

# Проверка работы Docker без sudo
docker --version
docker ps
```

## 📁 Подготовка проекта

### 1. Настройка Git
```bash
# Git уже установлен, настраиваем пользователя
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Настройка SSH для GitHub (если нужно)
ssh-keygen -t ed25519 -C "your.email@example.com"
cat ~/.ssh/id_ed25519.pub
# Скопируйте ключ и добавьте в GitHub Settings > SSH Keys
```

### 2. Создание директории проекта
```bash
# Создание директории для проекта
sudo mkdir -p /opt/habit_tracker
sudo chown $USER:$USER /opt/habit_tracker
cd /opt/habit_tracker

# Проверка прав доступа
ls -la /opt/
```

### 3. Клонирование репозитория
```bash
# Клонирование через HTTPS (проще для начала)
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git .

# ИЛИ через SSH (если настроили SSH ключ)
# git clone git@github.com:YOUR_USERNAME/YOUR_REPO_NAME.git .

# Проверка файлов
ls -la
```

## ⚙️ Настройка окружения

### 1. Создание файла переменных окружения
```bash
# Копирование шаблона
cp env_template .env

# Редактирование файла (используйте nano или vim)
nano .env
```

### 2. Заполнение .env файла
**ОБЯЗАТЕЛЬНО измените следующие параметры:**

```bash
# Django настройки
SECRET_KEY=your-super-secret-key-50-characters-long-change-this
DEBUG=False
ALLOWED_HOSTS=YOUR_SERVER_IP,your-domain.com

# База данных PostgreSQL
POSTGRES_DB=habit_tracker_prod
POSTGRES_USER=habit_user
POSTGRES_PASSWORD=STRONG_PASSWORD_CHANGE_THIS
DATABASE_URL=postgresql://habit_user:STRONG_PASSWORD_CHANGE_THIS@db:5432/habit_tracker_prod

# Telegram Bot
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 3. Настройка файрвола (безопасность)
```bash
# Установка UFW (если не установлен)
sudo apt install -y ufw

# Сброс правил к умолчанию
sudo ufw --force reset

# Запрет всех входящих соединений по умолчанию
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Разрешение SSH (ВАЖНО: сделайте это первым!)
sudo ufw allow ssh
sudo ufw allow 22/tcp

# Разрешение HTTP и HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Включение файрвола
sudo ufw --force enable

# Проверка статуса
sudo ufw status verbose
```

## 🚀 Первый запуск проекта

### 1. Запуск контейнеров
```bash
# Убедитесь, что находитесь в директории проекта
cd /opt/habit_tracker

# Первый запуск с построением образов
docker-compose -f docker-compose.prod.yml up -d --build

# Проверка статуса контейнеров (должны быть все "Up")
docker-compose -f docker-compose.prod.yml ps
```

### 2. Применение миграций базы данных
```bash
# Применение миграций Django
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Создание суперпользователя для админки
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 3. Проверка работоспособности
```bash
# Проверка логов (не должно быть ошибок)
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml logs nginx

# Проверка доступности сайта
curl http://localhost
curl http://YOUR_SERVER_IP
```

## 🔧 Настройка автоматического деплоя

### 1. Создание SSH ключа для GitHub Actions
```bash
# Создание отдельного SSH ключа для автоматического деплоя
ssh-keygen -t ed25519 -f ~/.ssh/github_actions -N ""

# Добавление публичного ключа в authorized_keys
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys

# Установка правильных прав
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/github_actions
chmod 644 ~/.ssh/github_actions.pub

# Вывод приватного ключа (СКОПИРУЙТЕ ЕГО!)
echo "=== ПРИВАТНЫЙ КЛЮЧ ДЛЯ GITHUB SECRETS ==="
cat ~/.ssh/github_actions
echo "=== КОНЕЦ КЛЮЧА ==="
```

### 2. Настройка GitHub Secrets
В вашем репозитории на GitHub перейдите в **Settings > Secrets and variables > Actions** и добавьте:

| Название | Значение | Описание |
|----------|----------|----------|
| `HOST` | `YOUR_SERVER_IP` | IP адрес вашего сервера |
| `USERNAME` | `ubuntu` | Имя пользователя SSH |
| `SSH_PRIVATE_KEY` | Содержимое `~/.ssh/github_actions` | Приватный SSH ключ |
| `SSH_PORT` | `22` | Порт SSH |
| `SECRET_KEY` | Ваш Django SECRET_KEY | Из .env файла |
| `POSTGRES_DB` | `habit_tracker_prod` | Имя базы данных |
| `POSTGRES_USER` | `habit_user` | Пользователь БД |
| `POSTGRES_PASSWORD` | Ваш пароль БД | Из .env файла |
| `DATABASE_URL` | Полная строка подключения | Из .env файла |
| `TELEGRAM_BOT_TOKEN` | Токен вашего бота | Из .env файла |
| `ALLOWED_HOSTS` | `YOUR_SERVER_IP,your-domain.com` | Разрешенные хосты |

### 3. Тестирование автоматического деплоя
После настройки секретов, любой push в ветку `main` будет автоматически разворачивать проект на сервере.

## 📊 Мониторинг и управление

### Основные команды для управления
```bash
# Просмотр статуса всех контейнеров
docker-compose -f docker-compose.prod.yml ps

# Просмотр логов в реальном времени
docker-compose -f docker-compose.prod.yml logs -f

# Перезапуск всех сервисов
docker-compose -f docker-compose.prod.yml restart

# Остановка всех сервисов
docker-compose -f docker-compose.prod.yml down

# Полная пересборка и запуск
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d --build
```

### Проверка ресурсов системы
```bash
# Использование ресурсов контейнерами
docker stats

# Использование диска
df -h

# Использование памяти
free -h

# Загрузка процессора
htop
```

## 🔧 Решение проблем

### Если контейнеры не запускаются
```bash
# Проверка логов с ошибками
docker-compose -f docker-compose.prod.yml logs

# Проверка конфигурации
docker-compose -f docker-compose.prod.yml config

# Принудительная пересборка
docker-compose -f docker-compose.prod.yml build --no-cache
```

### Если сайт недоступен
```bash
# Проверка портов
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# Проверка файрвола
sudo ufw status

# Проверка nginx
docker-compose -f docker-compose.prod.yml logs nginx
```

### Очистка системы от старых образов
```bash
# Удаление неиспользуемых образов и контейнеров
docker system prune -a

# Удаление неиспользуемых томов
docker volume prune
```

## 💰 Экономия средств Yandex Cloud

### Остановка ВМ когда не используется
```bash
# Перед остановкой ВМ - остановите контейнеры
docker-compose -f docker-compose.prod.yml down

# В веб-интерфейсе Yandex Cloud остановите ВМ
# ⚠️ ВНИМАНИЕ: IP адрес может измениться при перезапуске!
```

### Мониторинг расходов
- Регулярно проверяйте баланс в Yandex Cloud Console
- Настройте уведомления о превышении лимитов
- Используйте прерываемые ВМ для экономии (если подходит для ваших задач)

## ✅ Финальная проверка готовности

После завершения всех настроек проверьте:

1. **🌐 Сайт доступен:** `http://YOUR_SERVER_IP`
2. **📚 API документация:** `http://YOUR_SERVER_IP/api/docs/`
3. **⚙️ Админка Django:** `http://YOUR_SERVER_IP/admin/`
4. **🐳 Все контейнеры запущены:** `docker-compose -f docker-compose.prod.yml ps`
5. **📝 Логи без критических ошибок:** `docker-compose -f docker-compose.prod.yml logs`
6. **🔄 Автоматический деплой работает:** Push в main ветку

**🎉 Поздравляем! Ваш сервер полностью настроен и готов к работе!**

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи: `docker-compose -f docker-compose.prod.yml logs`
2. Убедитесь, что все переменные в `.env` заполнены правильно
3. Проверьте статус файрвола: `sudo ufw status`
4. Убедитесь, что Docker работает: `docker --version`