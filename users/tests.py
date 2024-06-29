from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersTestCase(APITestCase):
    def setUp(self):

        super().setUp()
        self.user = User.objects.create(
            email="new_email@list.ru", password="123q"
        )
        # print(self.user)

        self.client.force_authenticate(user=self.user)

    def test_login_is_true(self):
        """Проверка login (без ошибки)"""

        url = reverse("users:login")
        self.user = User.objects.create(
            email="em@list.ru", password=make_password("123qwe")
        )
        data = {"email": "em@list.ru", "password": "123qwe"}
        response = self.client.post(url, data=data)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.all().count(), 2)

    def test_login_is_false(self):
        """Проверка login (с ошибкой)"""

        url = reverse("users:login")

        data = {"email": "em@list.ru", "password": "1q"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        data = {"email": "123asd", "password": "12qwe"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve(self):
        """Проверка детализации"""

        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), self.user.email)

        url = reverse("users:user-detail", args=(101,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(data.get("email"), None)

    def test_create_is_true(self):
        """Проверка создания пользователя"""

        url = reverse("users:user-list")
        data = {"email": "create@list.ru", "password": "qwe"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.all().count(), 2)

    def test_create_is_false(self):
        """Проверка создания пользователя"""

        url = reverse("users:user-list")
        data = {"email": "create@list.ru"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.all().count(), 1)

    def test_update_is_false(self):
        """Проверка изменения пользователя (с ошибкой)"""

        url = reverse("users:user-detail", args=(self.user.pk,))
        data = {"email": "create@list.ru", "password": ""}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"password": ["This field may not be blank."]}
        )

    def test_delete_is_true(self):
        """Проверка удаления пользователя (без ошибки)"""

        url = reverse("users:user-detail", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.all().count(), 0)

    def test_delete_is_false(self):
        """Проверка удаления пользователя (с ошибкой)"""

        url = reverse("users:user-detail", args=(not self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.all().count(), 1)

    def test_list(self):
        """Проверка списка пользователей"""

        url = reverse("users:user-list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.user.pk,
                "email": self.user.email,
                "phone": None,
                "town": None,
                "tg_name": None,
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
