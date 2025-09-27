#!/usr/bin/env python3
"""
Скрипт для тестирования API эндпоинтов трекера привычек
"""

import requests
import json
import sys

API_BASE_URL = 'http://localhost:8000/api'

def test_api():
    """Тестирование основных API эндпоинтов"""
    
    print("🚀 Тестирование API трекера привычек")
    print("=" * 50)
    
    # Тестовые данные
    test_user = {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Тест",
        "last_name": "Пользователь",
        "password": "testpass123",
        "password_confirm": "testpass123"
    }
    
    token = None
    
    try:
        # 1. Тест регистрации
        print("\n1. 📝 Тестирование регистрации...")
        response = requests.post(f"{API_BASE_URL}/users/register/", json=test_user)
        
        if response.status_code == 201:
            data = response.json()
            token = data['token']
            print(f"✅ Регистрация успешна! Токен: {token[:20]}...")
        elif response.status_code == 400:
            print("⚠️  Пользователь уже существует, пробуем авторизацию...")
            
            # Пробуем авторизацию
            login_data = {
                "email": test_user["email"],
                "password": test_user["password"]
            }
            response = requests.post(f"{API_BASE_URL}/users/login/", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                token = data['token']
                print(f"✅ Авторизация успешна! Токен: {token[:20]}...")
            else:
                print(f"❌ Ошибка авторизации: {response.status_code}")
                return
        else:
            print(f"❌ Ошибка регистрации: {response.status_code}")
            print(response.text)
            return
        
        # Заголовки с токеном
        headers = {
            'Authorization': f'Token {token}',
            'Content-Type': 'application/json'
        }
        
        # 2. Тест профиля
        print("\n2. 👤 Тестирование профиля...")
        response = requests.get(f"{API_BASE_URL}/users/profile/", headers=headers)
        
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Профиль получен: {profile['email']}")
        else:
            print(f"❌ Ошибка получения профиля: {response.status_code}")
        
        # 3. Тест создания привычки
        print("\n3. 🎯 Тестирование создания привычки...")
        habit_data = {
            "place": "Кухня",
            "time": "08:00",
            "action": "Выпить стакан воды",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 30,
            "is_public": True,
            "reward": "Послушать музыку"
        }
        
        response = requests.post(f"{API_BASE_URL}/habits/", json=habit_data, headers=headers)
        
        if response.status_code == 201:
            habit = response.json()
            habit_id = habit['id']
            print(f"✅ Привычка создана: {habit['action']} (ID: {habit_id})")
        else:
            print(f"❌ Ошибка создания привычки: {response.status_code}")
            print(response.text)
            return
        
        # 4. Тест получения списка привычек
        print("\n4. 📋 Тестирование списка привычек...")
        response = requests.get(f"{API_BASE_URL}/habits/", headers=headers)
        
        if response.status_code == 200:
            habits_data = response.json()
            print(f"✅ Получено привычек: {habits_data['count']}")
            print(f"   Результатов на странице: {len(habits_data['results'])}")
        else:
            print(f"❌ Ошибка получения привычек: {response.status_code}")
        
        # 5. Тест создания приятной привычки
        print("\n5. 😊 Тестирование приятной привычки...")
        pleasant_habit_data = {
            "place": "Комната",
            "time": "08:05",
            "action": "Послушать любимую песню",
            "is_pleasant": True,
            "periodicity": 1,
            "execution_time": 180,
            "is_public": False
        }
        
        response = requests.post(f"{API_BASE_URL}/habits/", json=pleasant_habit_data, headers=headers)
        
        if response.status_code == 201:
            pleasant_habit = response.json()
            print(f"✅ Приятная привычка создана: {pleasant_habit['action']}")
        else:
            print(f"❌ Ошибка создания приятной привычки: {response.status_code}")
            print(response.text)
        
        # 6. Тест получения приятных привычек
        print("\n6. 🎵 Тестирование списка приятных привычек...")
        response = requests.get(f"{API_BASE_URL}/habits/pleasant_habits/", headers=headers)
        
        if response.status_code == 200:
            pleasant_habits = response.json()
            print(f"✅ Получено приятных привычек: {len(pleasant_habits)}")
            for habit in pleasant_habits:
                print(f"   - {habit['action']}")
        else:
            print(f"❌ Ошибка получения приятных привычек: {response.status_code}")
        
        # 7. Тест публичных привычек
        print("\n7. 🌍 Тестирование публичных привычек...")
        response = requests.get(f"{API_BASE_URL}/public-habits/", headers=headers)
        
        if response.status_code == 200:
            public_habits = response.json()
            print(f"✅ Получено публичных привычек: {public_habits['count']}")
        else:
            print(f"❌ Ошибка получения публичных привычек: {response.status_code}")
        
        # 8. Тест обновления привычки
        print("\n8. ✏️  Тестирование обновления привычки...")
        update_data = {
            "execution_time": 45,
            "place": "Столовая"
        }
        
        response = requests.patch(f"{API_BASE_URL}/habits/{habit_id}/", json=update_data, headers=headers)
        
        if response.status_code == 200:
            updated_habit = response.json()
            print(f"✅ Привычка обновлена: время выполнения {updated_habit['execution_time']} сек")
        else:
            print(f"❌ Ошибка обновления привычки: {response.status_code}")
        
        # 9. Тест документации
        print("\n9. 📚 Тестирование документации...")
        response = requests.get(f"{API_BASE_URL}/schema/")
        
        if response.status_code == 200:
            print("✅ OpenAPI схема доступна")
        else:
            print(f"❌ Ошибка получения схемы: {response.status_code}")
        
        print("\n" + "=" * 50)
        print("🎉 Тестирование завершено!")
        print(f"🔗 Swagger UI: http://localhost:8000/api/docs/")
        print(f"🔗 ReDoc: http://localhost:8000/api/redoc/")
        
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка подключения! Убедитесь, что Django сервер запущен:")
        print("   python manage.py runserver")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")

if __name__ == "__main__":
    test_api()
