from datetime import datetime

import pytz
from celery import shared_task

from config import settings
from habits.models import DaysOfWeek, Habit
from habits.services import send_telegram_message
from users.models import User


@shared_task
def send_email_about_new_habit(email, pk):
    """Направляет письмо о новой привычке"""

    user = User.objects.get(email=email)
    print(user)
    if user.tg_chat_id:
        habit = Habit.objects.filter(pk=pk).first()
        days = ",".join(
            DaysOfWeek.objects.filter(habit=habit).values_list(
                "name", flat=True
            )
        )

        message = (f"Вырабатываем новую привычку: {habit} "
                   f"по следующим дням: {days}.")
        print(message)
        send_telegram_message(user.tg_chat_id, message)


@shared_task
def send_reminder_email():
    """Направляет письмо - напоминание"""

    zone = pytz.timezone(settings.TIME_ZONE)
    # текущие дата и время
    current_datetime = datetime.now(zone)
    # день недели, начинается с 1
    day_of_week = current_datetime.weekday() + 1
    users = User.objects.all()
    for user in users:
        if user.tg_chat_id:
            # создание объекта рассылки, время отправки которого наступило
            habits = Habit.objects.filter(owner=user)
            for habit in habits:
                if (
                    habit.days.filter(pk=day_of_week)
                    and habit.start_time.hour == current_datetime.hour
                    and (habit.start_time.minute - 5) == current_datetime.minute
                ):
                    message = f"Напоминаю! Необходимо: {habit}."
                    send_telegram_message(user.tg_chat_id, message)
