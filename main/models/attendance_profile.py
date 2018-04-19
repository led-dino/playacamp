from django.db import models
from django.contrib.auth.models import User

from main.models.housing_group import HousingGroup
from main.models.job import Job
from main.models.transportation_method import TransportationMethod


class AttendanceProfile(models.Model):
    user = models.ForeignKey(User)
    year = models.IntegerField()

    housing_group = models.ForeignKey(HousingGroup, related_name='residents', null=True, blank=True)
    transportation_method = models.ForeignKey(TransportationMethod, related_name='attendees', null=True, blank=True)

    arrival_date = models.DateField(blank=True, null=True)
    departure_date = models.DateField(blank=True, null=True)

    has_early_pass = models.NullBooleanField(blank=True)
    has_ticket = models.NullBooleanField(blank=True)
    has_vehicle_pass = models.NullBooleanField(blank=True)
    paid_dues = models.BooleanField(default=False)

    bicycle_status = models.CharField(
        max_length=10,
        choices=(
            ('rent', 'Renting'),
            ('have', 'Have'),
            ('need', 'Need'),
        ),
        null=True,
        blank=True
    )

    job_preferences = models.ManyToManyField(Job, blank=True)
    shift_time_preference = models.CharField(
        max_length=10,
        choices=(
            ('day', 'Day shifts'),
            ('night', 'Evening shifts'),
            ('nopref', 'No preference'),
        ),
        null=True,
        blank=True
    )
    shift_day_preference = models.CharField(
        max_length=10,
        choices=(
            ('sameday', 'All same day'),
            ('b2b', 'Back to back days'),
            ('spread', 'Spread out'),
            ('nopref', 'No preference'),
        ),
        null=True,
        blank=True
    )

    def __str__(self):
        return '{}[{}]'.format(self.user, self.year)

