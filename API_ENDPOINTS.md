# API Эндпоинты для Трекера привычек

## Базовый URL
```
http://localhost:8000/api
```

## Аутентификация
Используется Token-based аутентификация. Токен передается в заголовке:
```
Authorization: Token <your-token-here>
```

---

## 👤 Пользователи (Users)

### 1. Регистрация пользователя
**POST** `/api/users/register/`

**Доступ:** Публичный

**Тело запроса:**
```json
{
    "email": "user@example.com",
    "username": "username",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "password": "password123",
    "password_confirm": "password123"
}
```

**Ответ (201):**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "telegram_chat_id": null
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### 2. Авторизация пользователя
**POST** `/api/users/login/`

**Доступ:** Публичный

**Тело запроса:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Ответ (200):**
```json
{
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "Имя",
        "last_name": "Фамилия",
        "telegram_chat_id": "123456789"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### 3. Просмотр профиля
**GET** `/api/users/profile/`

**Доступ:** Авторизованные пользователи

**Ответ (200):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "Имя",
    "last_name": "Фамилия",
    "telegram_chat_id": "123456789"
}
```

### 4. Обновление профиля
**PATCH** `/api/users/profile/`

**Доступ:** Авторизованные пользователи

**Тело запроса:**
```json
{
    "first_name": "Новое имя",
    "last_name": "Новая фамилия",
    "telegram_chat_id": "987654321"
}
```

**Ответ (200):**
```json
{
    "first_name": "Новое имя",
    "last_name": "Новая фамилия",
    "telegram_chat_id": "987654321"
}
```

---

## 🎯 Привычки пользователя (Habits)

### 5. Список привычек пользователя
**GET** `/api/habits/`

**Доступ:** Авторизованные пользователи

**Параметры запроса:**
- `page` - номер страницы (по умолчанию 1)
- `is_pleasant` - фильтр по приятным привычкам (true/false)
- `is_public` - фильтр по публичным привычкам (true/false)

**Пример:** `/api/habits/?page=1&is_pleasant=false`

**Ответ (200):**
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/habits/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": "user@example.com",
            "place": "Кухня",
            "time": "08:00:00",
            "action": "Выпить стакан воды",
            "is_pleasant": false,
            "related_habit": null,
            "periodicity": 1,
            "reward": "Послушать музыку",
            "execution_time": 30,
            "is_public": true,
            "created_at": "2023-12-01T08:00:00Z",
            "updated_at": "2023-12-01T08:00:00Z"
        }
    ]
}
```

### 6. Создание привычки
**POST** `/api/habits/`

**Доступ:** Авторизованные пользователи

**Тело запроса:**
```json
{
    "place": "Спортзал",
    "time": "18:00",
    "action": "Сделать 10 отжиманий",
    "is_pleasant": false,
    "related_habit": 2,
    "periodicity": 1,
    "reward": null,
    "execution_time": 60,
    "is_public": false
}
```

**Ответ (201):**
```json
{
    "id": 3,
    "user": "user@example.com",
    "place": "Спортзал",
    "time": "18:00:00",
    "action": "Сделать 10 отжиманий",
    "is_pleasant": false,
    "related_habit": 2,
    "periodicity": 1,
    "reward": null,
    "execution_time": 60,
    "is_public": false,
    "created_at": "2023-12-01T10:00:00Z",
    "updated_at": "2023-12-01T10:00:00Z"
}
```

### 7. Детали привычки
**GET** `/api/habits/{id}/`

**Доступ:** Владелец привычки

**Ответ (200):**
```json
{
    "id": 1,
    "user": "user@example.com",
    "place": "Кухня",
    "time": "08:00:00",
    "action": "Выпить стакан воды",
    "is_pleasant": false,
    "related_habit": null,
    "periodicity": 1,
    "reward": "Послушать музыку",
    "execution_time": 30,
    "is_public": true,
    "created_at": "2023-12-01T08:00:00Z",
    "updated_at": "2023-12-01T08:00:00Z"
}
```

### 8. Обновление привычки
**PATCH** `/api/habits/{id}/`

**Доступ:** Владелец привычки

**Тело запроса:**
```json
{
    "place": "Дом",
    "execution_time": 45,
    "is_public": true
}
```

**Ответ (200):** Обновленная привычка

### 9. Удаление привычки
**DELETE** `/api/habits/{id}/`

**Доступ:** Владелец привычки

**Ответ (204):** Нет содержимого

### 10. Список приятных привычек
**GET** `/api/habits/pleasant_habits/`

**Доступ:** Авторизованные пользователи

**Описание:** Возвращает список приятных привычек пользователя для выбора в связанных привычках

**Ответ (200):**
```json
[
    {
        "id": 2,
        "action": "Послушать музыку"
    },
    {
        "id": 4,
        "action": "Принять ванну"
    }
]
```

---

## 🌍 Публичные привычки (Public Habits)

### 11. Список публичных привычек
**GET** `/api/public-habits/`

**Доступ:** Авторизованные пользователи

**Параметры запроса:**
- `page` - номер страницы
- `user` - фильтр по пользователю (ID)

**Ответ (200):**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/public-habits/?page=2",
    "previous": null,
    "results": [
        {
            "id": 5,
            "user": "other@example.com",
            "place": "Парк",
            "time": "07:00:00",
            "action": "Утренняя пробежка",
            "periodicity": 1,
            "execution_time": 1800,
            "created_at": "2023-12-01T06:00:00Z"
        }
    ]
}
```

### 12. Детали публичной привычки
**GET** `/api/public-habits/{id}/`

**Доступ:** Авторизованные пользователи

**Ответ (200):** Детали публичной привычки (только для чтения)

---

## 📚 Документация API

### 13. OpenAPI схема
**GET** `/api/schema/`

**Доступ:** Публичный

**Ответ:** JSON схема OpenAPI 3.0

### 14. Swagger UI
**GET** `/api/docs/`

**Доступ:** Публичный

**Описание:** Интерактивная документация Swagger UI

### 15. ReDoc
**GET** `/api/redoc/`

**Доступ:** Публичный

**Описание:** Альтернативная документация ReDoc

---

## ⚠️ Валидация и ошибки

### Коды ошибок
- **400** - Неверные данные запроса
- **401** - Не авторизован
- **403** - Доступ запрещен
- **404** - Ресурс не найден
- **500** - Внутренняя ошибка сервера

### Примеры ошибок

**400 Bad Request:**
```json
{
    "password": ["Пароли не совпадают"],
    "execution_time": ["Убедитесь, что это значение меньше либо равно 120."]
}
```

**401 Unauthorized:**
```json
{
    "detail": "Учетные данные не были предоставлены."
}
```

**403 Forbidden:**
```json
{
    "detail": "У вас недостаточно прав для выполнения данного действия."
}
```

### Валидация привычек

1. **Время выполнения:** не более 120 секунд
2. **Периодичность:** от 1 до 7 дней
3. **Взаимоисключающие поля:** нельзя одновременно указывать `reward` и `related_habit`
4. **Связанные привычки:** только приятные привычки (`is_pleasant=true`)
5. **Приятные привычки:** не могут иметь `reward` или `related_habit`

---

## 🔧 Настройка CORS

Для работы с фронтендом настроены следующие CORS заголовки:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
```

---

## 📱 Интеграция с фронтендом

### JavaScript пример использования

```javascript
// Конфигурация
const API_BASE_URL = 'http://localhost:8000/api';
const authToken = localStorage.getItem('authToken');

// Функция для API запросов
async function apiRequest(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const config = {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    };
    
    if (authToken) {
        config.headers['Authorization'] = `Token ${authToken}`;
    }
    
    const response = await fetch(url, config);
    const data = await response.json();
    
    if (!response.ok) {
        throw new Error(data.detail || data.error || 'Произошла ошибка');
    }
    
    return data;
}

// Примеры использования
const habits = await apiRequest('/habits/');
const newHabit = await apiRequest('/habits/', {
    method: 'POST',
    body: JSON.stringify(habitData)
});
```

---

## 🚀 Запуск и тестирование

### Запуск сервера
```bash
python manage.py runserver
```

### Тестирование с curl

**Регистрация:**
```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

**Получение привычек:**
```bash
curl -X GET http://localhost:8000/api/habits/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Тестирование с фронтендом
1. Запустите Django сервер: `python manage.py runserver`
2. Откройте `frontend/index.html` в браузере
3. Зарегистрируйтесь или войдите в систему
4. Создавайте и управляйте привычками через интерфейс

---

## 📊 Пагинация

Все списочные эндпоинты поддерживают пагинацию:
- **Размер страницы:** 5 элементов
- **Параметр:** `?page=N`
- **Ответ содержит:** `count`, `next`, `previous`, `results`

---

## 🔐 Безопасность

1. **Аутентификация:** Token-based
2. **Авторизация:** Пользователи видят только свои привычки
3. **CORS:** Настроен для разрешенных доменов
4. **Валидация:** Серверная валидация всех данных
5. **Права доступа:** Строгое разделение прав на объекты

