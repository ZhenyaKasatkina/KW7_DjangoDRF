from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class DaysOfWeek(models.Model):
    """Дни недели"""

    MO = "пн"
    TU = "вт"
    WE = "ср"
    TH = "чт"
    FR = "пт"
    SA = "сб"
    SU = "вс"
    DAYS = {
        MO: "пн",
        TU: "вт",
        WE: "ср",
        TH: "чт",
        FR: "пт",
        SA: "сб",
        SU: "вс"}
    name = models.CharField(
        choices=DAYS, max_length=2, verbose_name="Дни недели", default=MO
    )

    def __str__(self):
        return self.name

    class Meta:
        # Настройка для наименования одного объекта
        verbose_name = "день"
        # Настройка для наименования набора объектов
        verbose_name_plural = "дни"


class Habit(models.Model):
    """Привычка"""

    owner = models.ForeignKey(
        User,
        related_name="habit",
        verbose_name="создатель привычки",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )
    place = models.CharField(
        max_length=150,
        verbose_name="Место",
        help_text="место, в котором необходимо выполнять привычку",
    )
    action = models.CharField(
        max_length=150,
        verbose_name="Действие",
        help_text="действие, которое представляет собой привычка,"
        "Отвечает на вопрос: 'Что делать?'.",
    )

    ONCE_A_DAY = "Каждый день"
    DAYS_OF_WEEK = "Выбрать дни недели"
    PERIODICITY = {
        ONCE_A_DAY: "Каждый день",
        DAYS_OF_WEEK: "Выбрать дни недели",
    }
    periodicity = models.CharField(
        choices=PERIODICITY,
        max_length=30,
        verbose_name="Периодичность",
        default=ONCE_A_DAY,
    )
    days = models.ManyToManyField(
        DaysOfWeek,
        verbose_name="Выбор дней недели",
        related_name="habit",
        help_text="Выбери дни недели",
    )
    start_time = models.TimeField(
        verbose_name="Время начала действия",
        help_text="время, когда необходимо выполнять привычку",
    )
    is_enjoyable = models.BooleanField(
        verbose_name="Признак приятной привычки", default=False
    )
    associated_habit = models.ForeignKey(
        "self",
        related_name="useful_habit",
        verbose_name="связанная привычка",
        on_delete=models.CASCADE,
        help_text="указывать только для полезных привычек",
        **NULLABLE,
    )
    reward = models.TextField(
        max_length=150,
        verbose_name="Вознаграждение",
        **NULLABLE,
        help_text="чем пользователь должен себя вознаградить после выполнения",
    )
    time_to_complete = models.PositiveIntegerField(
        default=120,
        validators=[MaxValueValidator(120)],
        verbose_name="Время выполнения действия",
        help_text="время на выполнение привычки (в секундах)",
    )
    is_public = models.BooleanField(
        default=False,
        verbose_name="Статус публичности"
    )

    def __str__(self):
        # Строковое отображение объекта
        return (
            f"{self.action} {self.place} в {self.start_time} "
            f"(в течении {self.time_to_complete} секунд)"
        )

    class Meta:
        # Настройка для наименования одного объекта
        verbose_name = "привычка"
        # Настройка для наименования набора объектов
        verbose_name_plural = "привычки"
        # Сортировка по id
        ordering = ["-pk"]
