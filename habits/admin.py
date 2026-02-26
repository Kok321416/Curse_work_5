from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    """Админка для модели привычки"""

    list_display = (
        'action', 'user', 'place', 'time', 'is_pleasant',
        'periodicity', 'execution_time', 'is_public', 'created_at'
    )
    list_filter = ('is_pleasant', 'is_public', 'periodicity', 'created_at')
    search_fields = ('action', 'place', 'user__email')
    list_editable = ('is_public',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'action', 'place', 'time')
        }),
        ('Настройки привычки', {
            'fields': ('is_pleasant', 'related_habit', 'reward', 'execution_time', 'periodicity')
        }),
        ('Публичность', {
            'fields': ('is_public',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """Оптимизация запросов"""
        return super().get_queryset(request).select_related('user', 'related_habit')
