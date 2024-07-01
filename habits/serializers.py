from rest_framework import serializers

from habits.models import Habit
from users.serializers import UserSerializer


class HabitSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def validate(self, attrs):

        if "associated_habit" in attrs:
            if not attrs["associated_habit"].is_enjoyable:
                raise serializers.ValidationError(
                    "Можно добавить только приятную привычку"
                )
            if attrs["associated_habit"].is_enjoyable:
                if "reward" in attrs and "associated_habit" in attrs:
                    raise serializers.ValidationError(
                        "Одновременно приятную привычку "
                        "и вознаграждение добавлять нельзя"
                    )

        if attrs["is_enjoyable"]:
            if "reward" in attrs:
                raise serializers.ValidationError(
                    "За приятную привычку вознаграждение не предусмотрено"
                )
            if "associated_habit" in attrs:
                raise serializers.ValidationError(
                    "У приятной привычки нет еще одной приятной привычки"
                )

        if (attrs["periodicity"] == "Каждый день" and
                len(set(attrs["days"])) < 7):
            raise serializers.ValidationError(
                "Необходимо выбрать все дни недели"
            )

        return attrs

    class Meta:
        model = Habit
        fields = "__all__"
