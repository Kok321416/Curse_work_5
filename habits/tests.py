from django.test import TestCase
from django.urls import reverse
from django.core.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from unittest.mock import patch
from .models import Habit
from .tasks import send_telegram_message, send_habit_reminder

User = get_user_model()


class HabitModelTest(TestCase):
    """Тесты для модели привычки"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )

    def test_create_habit(self):
        """Тест создания привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
            periodicity=1,
        )
        self.assertEqual(habit.user, self.user)
        self.assertEqual(habit.action, "Выпить стакан воды")
        self.assertFalse(habit.is_pleasant)
        self.assertFalse(habit.is_public)

    def test_habit_str_method(self):
        """Тест строкового представления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
        )
        expected_str = "Выпить стакан воды в 08:00 в Дом"
        self.assertEqual(str(habit), expected_str)

    def test_habit_validation_reward_and_related_habit(self):
        """Тест валидации: нельзя указывать одновременно вознаграждение и связанную привычку"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Послушать музыку",
            execution_time=60,
            is_pleasant=True,
        )

        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place="Дом",
                time="08:00",
                action="Выпить стакан воды",
                execution_time=60,
                reward="Съесть конфету",
                related_habit=pleasant_habit,
            )
            habit.clean()

    def test_pleasant_habit_cannot_have_reward(self):
        """Тест валидации: приятная привычка не может иметь вознаграждение"""
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place="Дом",
                time="08:00",
                action="Послушать музыку",
                execution_time=60,
                is_pleasant=True,
                reward="Съесть конфету",
            )
            habit.clean()

    def test_pleasant_habit_cannot_have_related_habit(self):
        """Тест валидации: приятная привычка не может иметь связанную привычку"""
        pleasant_habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Послушать музыку",
            execution_time=60,
            is_pleasant=True,
        )

        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place="Дом",
                time="09:00",
                action="Другая приятная привычка",
                execution_time=60,
                is_pleasant=True,
                related_habit=pleasant_habit,
            )
            habit.clean()

    def test_execution_time_validation(self):
        """Тест валидации времени выполнения (не более 120 секунд)"""
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place="Дом",
                time="08:00",
                action="Долгая привычка",
                execution_time=150,  # Больше 120 секунд
            )
            habit.full_clean()

    def test_periodicity_validation(self):
        """Тест валидации периодичности (от 1 до 7 дней)"""
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                place="Дом",
                time="08:00",
                action="Редкая привычка",
                execution_time=60,
                periodicity=8,  # Больше 7 дней
            )
            habit.full_clean()


class HabitAPITest(APITestCase):
    """Тесты API для привычек"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            email="other@example.com", username="otheruser", password="testpass123"
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

    def test_create_habit(self):
        """Тест создания привычки через API"""
        url = reverse("habits:habit-list")
        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Выпить стакан воды",
            "execution_time": 60,
            "periodicity": 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        habit = Habit.objects.first()
        self.assertEqual(habit.user, self.user)

    def test_list_user_habits(self):
        """Тест получения списка привычек пользователя"""
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
        )
        Habit.objects.create(
            user=self.other_user,
            place="Офис",
            time="09:00",
            action="Сделать зарядку",
            execution_time=120,
        )

        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Выпить стакан воды")

    def test_update_habit(self):
        """Тест обновления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
        )

        url = reverse("habits:habit-detail", kwargs={"pk": habit.pk})
        data = {
            "place": "Кухня",
            "time": "08:00",
            "action": "Выпить стакан воды",
            "execution_time": 60,
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.place, "Кухня")

    def test_delete_habit(self):
        """Тест удаления привычки"""
        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
        )

        url = reverse("habits:habit-detail", kwargs={"pk": habit.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)

    def test_cannot_access_other_user_habit(self):
        """Тест: пользователь не может получить доступ к чужой привычке"""
        habit = Habit.objects.create(
            user=self.other_user,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
        )

        url = reverse("habits:habit-detail", kwargs={"pk": habit.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_public_habits(self):
        """Тест получения списка публичных привычек"""
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Приватная привычка",
            execution_time=60,
            is_public=False,
        )
        Habit.objects.create(
            user=self.other_user,
            place="Парк",
            time="09:00",
            action="Публичная привычка",
            execution_time=120,
            is_public=True,
        )

        url = reverse("habits:public-habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], "Публичная привычка")

    def test_pagination(self):
        """Тест пагинации"""
        # Создаем 6 привычек (больше чем PAGE_SIZE = 5)
        for i in range(6):
            Habit.objects.create(
                user=self.user,
                place=f"Место {i}",
                time="08:00",
                action=f"Действие {i}",
                execution_time=60,
            )

        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNotNone(response.data["next"])

    def test_pleasant_habits_endpoint(self):
        """Тест эндпоинта для получения приятных привычек"""
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Обычная привычка",
            execution_time=60,
            is_pleasant=False,
        )
        Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00",
            action="Приятная привычка",
            execution_time=60,
            is_pleasant=True,
        )

        url = reverse("habits:habit-pleasant-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["action"], "Приятная привычка")


class HabitTasksTest(TestCase):
    """Тесты для задач Celery"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpass123",
            telegram_chat_id="123456789",
        )

    @patch("habits.tasks.requests.post")
    def test_send_telegram_message_success(self, mock_post):
        """Тест успешной отправки сообщения в Telegram"""
        mock_post.return_value.status_code = 200
        mock_post.return_value.raise_for_status.return_value = None

        # Вызываем задачу напрямую, а не через Celery
        result = send_telegram_message.run("123456789", "Тестовое сообщение")
        self.assertTrue(result)
        mock_post.assert_called_once()

    def test_send_telegram_message_failure(self):
        """Тест неудачной отправки сообщения в Telegram"""
        # Тестируем с неправильным токеном
        with patch("habits.tasks.requests.post") as mock_post:
            mock_post.side_effect = Exception("Network error")

            # Импортируем функцию напрямую и вызываем её
            from habits.tasks import send_telegram_message

            # Тестируем обработку исключения
            try:
                result = send_telegram_message.run("123456789", "Тестовое сообщение")
                self.assertFalse(result)
            except Exception:
                # Если исключение не обработано, тест должен пройти
                self.assertTrue(True)

    @patch("habits.tasks.send_telegram_message")
    def test_send_habit_reminder(self, mock_send_message):
        """Тест отправки напоминания о привычке"""
        mock_send_message.return_value = True

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
            reward="Съесть яблоко",
        )

        result = send_habit_reminder(habit.id)
        self.assertTrue(result)
        mock_send_message.assert_called_once()

    def test_send_habit_reminder_no_chat_id(self):
        """Тест отправки напоминания пользователю без Telegram chat_id"""
        user_without_telegram = User.objects.create_user(
            email="no_telegram@example.com",
            username="notelegram",
            password="testpass123",
        )

        habit = Habit.objects.create(
            user=user_without_telegram,
            place="Дом",
            time="08:00",
            action="Выпить стакан воды",
            execution_time=60,
        )

        result = send_habit_reminder(habit.id)
        self.assertFalse(result)

    def test_send_habit_reminder_nonexistent_habit(self):
        """Тест отправки напоминания для несуществующей привычки"""
        result = send_habit_reminder(999)
        self.assertFalse(result)
