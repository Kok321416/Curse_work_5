from celery import shared_task
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
import requests
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_telegram_message(chat_id, message):
    """Отправка сообщения в Telegram"""
    
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.error("Telegram bot token не настроен")
        return False
    
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        logger.info(f"Сообщение отправлено в чат {chat_id}")
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка отправки сообщения в Telegram: {e}")
        return False


@shared_task
def send_habit_reminder(habit_id):
    """Отправка напоминания о привычке"""
    
    from .models import Habit
    
    try:
        habit = Habit.objects.select_related('user').get(id=habit_id)
    except Habit.DoesNotExist:
        logger.error(f"Привычка с ID {habit_id} не найдена")
        return False
    
    if not habit.user.telegram_chat_id:
        logger.warning(f"У пользователя {habit.user.email} не настроен Telegram chat_id")
        return False
    
    message = (
        f"🔔 <b>Напоминание о привычке!</b>\n\n"
        f"📍 <b>Действие:</b> {habit.action}\n"
        f"🕐 <b>Время:</b> {habit.time.strftime('%H:%M')}\n"
        f"📍 <b>Место:</b> {habit.place}\n"
        f"⏱ <b>Время выполнения:</b> {habit.execution_time} сек."
    )
    
    if habit.reward:
        message += f"\n🎁 <b>Вознаграждение:</b> {habit.reward}"
    elif habit.related_habit:
        message += f"\n😊 <b>Приятная привычка:</b> {habit.related_habit.action}"
    
    return send_telegram_message(habit.user.telegram_chat_id, message)


@shared_task
def schedule_habit_reminders():
    """Планирование напоминаний о привычках на следующие 24 часа"""
    
    from .models import Habit
    from django_celery_beat.models import PeriodicTask, CrontabSchedule
    import json
    
    now = timezone.now()
    tomorrow = now + timedelta(days=1)
    
    # Получаем все активные привычки пользователей с настроенным Telegram
    habits = Habit.objects.filter(
        user__telegram_chat_id__isnull=False,
        user__telegram_chat_id__gt=''
    ).select_related('user')
    
    scheduled_count = 0
    
    for habit in habits:
        # Вычисляем следующее время выполнения привычки
        habit_time = datetime.combine(now.date(), habit.time)
        
        # Если время уже прошло сегодня, планируем на завтра
        if habit_time <= now:
            habit_time = datetime.combine(tomorrow.date(), habit.time)
        
        # Проверяем периодичность
        days_since_creation = (now.date() - habit.created_at.date()).days
        if days_since_creation % habit.periodicity != 0:
            continue
        
        # Создаем задачу напоминания
        task_name = f"habit_reminder_{habit.id}_{habit_time.strftime('%Y%m%d_%H%M')}"
        
        # Проверяем, не создана ли уже такая задача
        if not PeriodicTask.objects.filter(name=task_name).exists():
            # Создаем расписание
            schedule, created = CrontabSchedule.objects.get_or_create(
                minute=habit_time.minute,
                hour=habit_time.hour,
                day_of_month=habit_time.day,
                month_of_year=habit_time.month,
            )
            
            # Создаем периодическую задачу
            PeriodicTask.objects.create(
                crontab=schedule,
                name=task_name,
                task='habits.tasks.send_habit_reminder',
                args=json.dumps([habit.id]),
                one_off=True,  # Выполнить только один раз
            )
            
            scheduled_count += 1
    
    logger.info(f"Запланировано {scheduled_count} напоминаний о привычках")
    return scheduled_count
