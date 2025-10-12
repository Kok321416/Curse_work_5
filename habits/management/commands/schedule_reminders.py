from django.core.management.base import BaseCommand
from habits.tasks import schedule_habit_reminders


class Command(BaseCommand):
    help = "Планирование напоминаний о привычках"

    def handle(self, *args, **options):
        count = schedule_habit_reminders()
        self.stdout.write(
            self.style.SUCCESS(f"Успешно запланировано {count} напоминаний о привычках")
        )
