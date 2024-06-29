from django.urls import path

from habits.apps import HabitsConfig
from habits.permissions import IsOwner
from habits.views import (HabitCreateAPIView, HabitDestroyAPIView,
                          HabitListAPIView, HabitUpdateAPIView,
                          PublicHabitListAPIView)

app_name = HabitsConfig.name

urlpatterns = [
    path(
        "habit/",
        HabitListAPIView.as_view(permission_classes=(IsOwner,)),
        name="habit_list",
    ),
    path(
        "public_habit/",
        PublicHabitListAPIView.as_view(),
        name="public_habits_list"
    ),
    path(
        "habit/create/",
        HabitCreateAPIView.as_view(),
        name="habit_create"
    ),
    path(
        "habit/<int:pk>/update/",
        HabitUpdateAPIView.as_view(permission_classes=(IsOwner,)),
        name="habit_update",
    ),
    path(
        "habit/<int:pk>/delete/",
        HabitDestroyAPIView.as_view(permission_classes=(IsOwner,)),
        name="habit_delete",
    ),
]
