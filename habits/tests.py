from django.core import management
from django.core.management.commands import loaddata
from django.urls import reverse
from django.utils import translation
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from habits.models import Habit
from users.models import User


class HabitsTestCase(APITestCase):
    def setUp(self) -> None:

        super().setUp()
        self.user = User.objects.create(email="new_email@list.ru")
        management.call_command(loaddata.Command(), "days.json")
        self.enjoyable_habit = Habit.objects.create(
            owner=self.user,
            place="на работе",
            periodicity="Выбрать дни недели",
            action="съесть яблоко",
            start_time="13:00:00",
            is_enjoyable="True",
            time_to_complete=120,
            is_public=True,
        )
        self.enjoyable_habit.save()
        self.enjoyable_habit.days.add(6, 7)

        self.client.force_authenticate(user=self.user)

    def test_habit_create_is_true(self):
        """Проверка создания привычки (без ошибки)"""

        url = reverse("habits:habit_create")
        data = {
            "place": "на работе",
            "periodicity": "Каждый день",
            "action": "проверить результат работы за день",
            "start_time": "16:40:00",
            "is_enjoyable": "False",
            "days": [1, 2, 3, 4, 5, 6, 7],
            "reward": "похвалить себя и коллег",
            "time_to_complete": 120,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_habit_create_is_false(self):
        """Проверка создания привычки (с ошибкой)"""

        url = reverse("habits:habit_create")

        # приятная привычка не имеет вознаграждение
        data = {
            "place": "на работе",
            "periodicity": "Каждый день",
            "days": [1, 2, 3, 4, 5, 6, 7],
            "action": "проверить результат работы за день",
            "start_time": "16:40:00",
            "is_enjoyable": "True",
            "reward": "похвалить себя и коллег",
            "time_to_complete": 120,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

        # полезная привычка не имеет и вознаграждение и приятную привычку
        data = {
            "place": "на работе",
            "periodicity": "Каждый день",
            "days": [1, 2, 3, 4, 5, 6, 7],
            "action": "проверить результат работы за день",
            "start_time": "16:40:00",
            "is_enjoyable": "False",
            "associated_habit": 2,
            "reward": "похвалить себя и коллег",
            "time_to_complete": 120,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

        # не соблюден срок на действия привычки
        data = {
            "place": "на работе",
            "periodicity": "Каждый день",
            "days": [1, 2, 3, 4, 5, 6, 7],
            "action": "проверить результат работы за день",
            "start_time": "16:40:00",
            "is_enjoyable": "False",
            "reward": "похвалить себя и коллег",
            "time_to_complete": 130,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

        # не верные дни недели
        data = {
            "place": "на работе",
            "periodicity": "Каждый день",
            "days": [2, 3, 4, 5, 6, 7],
            "action": "проверить результат работы за день",
            "start_time": "16:40:00",
            "is_enjoyable": "False",
            "reward": "похвалить себя и коллег",
            "time_to_complete": 120,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

        data = {
            "place": "на работе",
            "periodicity": "Выбрать дни недели",
            "days": [],
            "action": "проверить результат работы за день",
            "start_time": "16:40:00",
            "is_enjoyable": "False",
            "reward": "похвалить себя и коллег",
            "time_to_complete": 120,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_update_is_true(self):
        """Проверка изменения привычки (без ошибки)"""

        url = reverse("habits:habit_update", args=(self.enjoyable_habit.pk,))
        data = {
            "place": "дома",
            "periodicity": "Каждый день",
            "days": [1, 2, 3, 4, 5, 6, 7],
            "action": "съесть яблоко",
            "start_time": "13:40:00",
            "is_enjoyable": False,
            "reward": "null",
            "time_to_complete": 120,
        }

        response = self.client.put(url, data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("place"), data["place"])

    def test_habit_update_is_false(self):
        """Проверка изменения привычки (с ошибкой)"""

        url = reverse("habits:habit_update", args=(self.enjoyable_habit.pk,))
        data = {"reward": "null", "time_to_complete": 120}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.enjoyable_habit.reward, None)

    def test_habit_delete_is_true(self):
        """Проверка удаления привычки (без ошибки)"""

        url = reverse("habits:habit_delete", args=(self.enjoyable_habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_habit_delete_is_false(self):
        """Проверка удаления привычки (с ошибкой)"""

        url = reverse("habits:habit_delete", args=(101,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_list_is_true(self):
        """Проверка списка привычек"""

        url = reverse("habits:habit_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.enjoyable_habit.pk,
                    "place": "на работе",
                    "action": "съесть яблоко",
                    "periodicity": "Выбрать дни недели",
                    "start_time": "13:00:00",
                    "is_enjoyable": True,
                    "reward": None,
                    "time_to_complete": 120,
                    "is_public": True,
                    "owner": self.user.pk,
                    "associated_habit": None,
                    "days": [6, 7],
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_public_habits_list_is_true(self):
        """Проверка списка привычек"""

        url = reverse("habits:public_habits_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.enjoyable_habit.pk,
                    "place": "на работе",
                    "action": "съесть яблоко",
                    "periodicity": "Выбрать дни недели",
                    "start_time": "13:00:00",
                    "is_enjoyable": True,
                    "reward": None,
                    "time_to_complete": 120,
                    "is_public": True,
                    "owner": self.user.pk,
                    "associated_habit": None,
                    "days": [6, 7],
                },
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)
        super().tearDown()
