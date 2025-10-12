from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from habits.models import Habit

User = get_user_model()


def health_check(request):
    """Health check endpoint для мониторинга"""
    return JsonResponse({"status": "ok", "message": "Application is running"})


def home_view(request):
    """Главная страница с навигацией по API"""
    return render(request, "home.html")


def demo_view(request):
    """Демо страница с реальными данными"""
    context = {
        "users_count": User.objects.count(),
        "habits_count": Habit.objects.count(),
        "public_habits_count": Habit.objects.filter(is_public=True).count(),
        "pleasant_habits_count": Habit.objects.filter(is_pleasant=True).count(),
        "public_habits": Habit.objects.filter(is_public=True).select_related(
            "user", "related_habit"
        )[:6],
        "all_habits": Habit.objects.all().select_related("user", "related_habit")[:10],
    }
    return render(request, "demo.html", context)
