from datetime import datetime, timedelta

from django.utils import timezone


def find_labor_day_for_year(year: int) -> datetime:
    monday = 0
    august = 8
    last_day_of_august = datetime(year=year, month=august, day=31, tzinfo=timezone.get_current_timezone())
    days_ahead = monday - last_day_of_august.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return last_day_of_august + timedelta(days_ahead)


def get_next_event_year() -> int:
    now = timezone.now()
    year = now.year
    labor_day = find_labor_day_for_year(year)
    if now > labor_day:
        year += 1
    return year
