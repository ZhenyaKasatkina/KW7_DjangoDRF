from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Пользователь"""

    username = None
    email = models.EmailField(
        unique=True, verbose_name="Адрес электронной почты"
    )
    phone = models.CharField(
        max_length=35, verbose_name="телефон", **NULLABLE
    )
    town = models.CharField(
        max_length=100, verbose_name="город", **NULLABLE
    )
    avatar = models.ImageField(
        upload_to="users/avatars/", verbose_name="аватарка", **NULLABLE
    )
    tg_name = models.CharField(
        max_length=50, verbose_name="Ник Телеграм", **NULLABLE
    )
    tg_chat_id = models.CharField(
        max_length=50, verbose_name="Телеграм chat_id", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        # Строковое отображение объекта
        return f"{self.email}"

    class Meta:
        # Настройка для наименования одного объекта
        verbose_name = "пользователь"
        # Настройка для наименования набора объектов
        verbose_name_plural = "пользователи"
