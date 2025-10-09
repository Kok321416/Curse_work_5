from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Админка для кастомной модели пользователя"""

    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "telegram_chat_id",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "date_joined")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ("email",)

    fieldsets = UserAdmin.fieldsets + (("Telegram", {"fields": ("telegram_chat_id",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": ("email", "telegram_chat_id"),
            },
        ),
    )
