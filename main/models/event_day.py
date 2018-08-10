from enum import Enum
from typing import List


class EventDay(Enum):
    Wednesday1 = 1
    Thursday1 = 2
    Friday1 = 3
    Saturday1 = 4
    Sunday1 = 5
    Monday1 = 6
    Tuesday1 = 7
    Wednesday2 = 8
    Thursday2 = 9
    Friday2 = 10
    Saturday2 = 11
    Sunday2 = 12
    Monday2 = 13
    Tuesday2 = 14


EVENT_DAY_BY_ARRIVAL_CHOICES = {
    'wednesday1': EventDay.Wednesday1,
    'thursday1': EventDay.Thursday1,
    'friday1': EventDay.Friday1,
    'saturday': EventDay.Saturday1,
    'sunday': EventDay.Sunday1,
    'monday': EventDay.Monday1,
    'tuesday': EventDay.Tuesday1,
    'wednesday2': EventDay.Wednesday2,
    'thursday2': EventDay.Thursday2,
    'friday2': EventDay.Friday2,
}

EVENT_DAY_BY_DEPARTURE_CHOICES = {
    'wednesday': EventDay.Wednesday2,
    'thursday': EventDay.Thursday2,
    'friday': EventDay.Friday2,
    'saturday': EventDay.Saturday2,
    'sunday': EventDay.Sunday2,
    'monday': EventDay.Monday2,
    'tuesday': EventDay.Tuesday2,
}


def days_between(start_day: EventDay, end_day: EventDay) -> List[EventDay]:
    return [day for day in EventDay if start_day.value <= day.value < end_day.value]
