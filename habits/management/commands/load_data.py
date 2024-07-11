from django.core.management.base import BaseCommand
import json
from habits.models import DaysOfWeek


class Command(BaseCommand):
    def handle(self, *args, **options):

        with open('days.json', 'rb') as f:
            data = json.load(f)

            for i in data:
                print(i)
                day = DaysOfWeek()
                day.name = i['fields']['name']
                day.save()

        print('finished')
