from collections import defaultdict
from typing import Dict

from django.core.management.base import BaseCommand, CommandError

from main.models import AttendanceProfile
from main.models.event_day import EVENT_DAY_BY_ARRIVAL_CHOICES, EVENT_DAY_BY_DEPARTURE_CHOICES, days_between, EventDay


class Command(BaseCommand):
    help = 'Prints attendance counts by day'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)

    def handle(self, *args, **options):
        year = options['year']
        attendance_profiles = AttendanceProfile.objects.filter(year=year, deleted_at__isnull=True)
        count_by_day = defaultdict(int)  # type: Dict[str, int]
        for attendance_profile in attendance_profiles:
            if attendance_profile.arrival_date is None or attendance_profile.departure_date is None:
                continue
            arrival_day = EVENT_DAY_BY_ARRIVAL_CHOICES[attendance_profile.arrival_date]
            departure_day = EVENT_DAY_BY_DEPARTURE_CHOICES[attendance_profile.departure_date]

            for day in days_between(arrival_day, departure_day):
                count_by_day[day.name] += 1

        for day in EventDay:
            count = count_by_day.get(day.name, 0)
            self.stdout.write("{}: {}\n".format(day.name, count))
