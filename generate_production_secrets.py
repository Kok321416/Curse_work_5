#!/usr/bin/env python3
"""
Скрипт для генерации секретов для продакшена
"""
import secrets
import string

def generate_secret_key():
    """Генерирует Django SECRET_KEY"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*(-_=+)'
    return ''.join(secrets.choice(chars) for _ in range(50))

def generate_password():
    """Генерирует пароль для базы данных"""
    chars = string.ascii_letters + string.digits
    return ''.join(secrets.choice(chars) for _ in range(20))

if __name__ == "__main__":
    print("=== СЕКРЕТЫ ДЛЯ GITHUB ACTIONS ===")
    print()
    
    secret_key = generate_secret_key()
    postgres_password = generate_password()
    
    print("SECRET_KEY:")
    print(secret_key)
    print()
    
    print("ALLOWED_HOSTS:")
    print("158.160.202.67,localhost")
    print()
    
    print("POSTGRES_DB:")
    print("habit_tracker")
    print()
    
    print("POSTGRES_USER:")
    print("postgres")
    print()
    
    print("POSTGRES_PASSWORD:")
    print(postgres_password)
    print()
    
    print("DATABASE_URL:")
    print(f"postgresql://postgres:{postgres_password}@db:5432/habit_tracker")
    print()
    
    print("TELEGRAM_BOT_TOKEN:")
    print("ВАШ_ТОКЕН_БОТА (получите у @BotFather)")
    print()
    
    print("=== СКОПИРУЙТЕ ЭТИ ЗНАЧЕНИЯ В GITHUB SECRETS ===")
