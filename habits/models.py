from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Habit(models.Model):
    """Модель привычки"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="habits",
    )
    place = models.CharField(
        max_length=200,
        verbose_name="Место выполнения",
        help_text="Место, в котором необходимо выполнять привычку",
    )
    time = models.TimeField(
        verbose_name="Время выполнения",
        help_text="Время, когда необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=200,
        verbose_name="Действие",
        help_text="Действие, которое представляет собой привычка",
    )
    is_pleasant = models.BooleanField(
        default=False,
        verbose_name="Признак приятной привычки",
        help_text="Привычка, которую можно привязать к выполнению полезной привычки",
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
        help_text="Привычка, которая связана с другой привычкой",
        limit_choices_to={"is_pleasant": True},
    )
    periodicity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name="Периодичность в днях",
        help_text="Периодичность выполнения привычки для напоминания в днях (от 1 до 7)",
    )
    reward = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Вознаграждение",
        help_text="Чем пользователь должен себя вознаградить после выполнения",
    )
    execution_time = models.PositiveIntegerField(
        validators=[MaxValueValidator(120)],
        verbose_name="Время на выполнение в секундах",
        help_text="Время, которое предположительно потратит пользователь на выполнение привычки (не более 120 секунд)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Признак публичности",
        help_text="Привычки можно публиковать в общий доступ",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]

    def __str__(self):
        if hasattr(self.time, "strftime"):
            time_str = self.time.strftime("%H:%M")
        else:
            time_str = str(self.time)
        return f"{self.action} в {time_str} в {self.place}"

    def clean(self):
        """Валидация модели"""
        errors = {}

        # Исключить одновременный выбор связанной привычки и указания вознаграждения
        if self.related_habit and self.reward:
            errors["related_habit"] = (
                "Нельзя одновременно указывать связанную привычку и вознаграждение"
            )
            errors["reward"] = (
                "Нельзя одновременно указывать связанную привычку и вознаграждение"
            )

        # В связанные привычки могут попадать только привычки с признаком приятной привычки
        if self.related_habit and not self.related_habit.is_pleasant:
            errors["related_habit"] = (
                "В связанные привычки могут попадать только приятные привычки"
            )

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant:
            if self.reward:
                errors["reward"] = "У приятной привычки не может быть вознаграждения"
            if self.related_habit:
                errors["related_habit"] = (
                    "У приятной привычки не может быть связанной привычки"
                )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        """Переопределение метода save для вызова валидации"""
        self.clean()
        super().save(*args, **kwargs)
