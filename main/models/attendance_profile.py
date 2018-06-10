from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, CheckboxSelectMultiple

from main.models.housing_group import HousingGroup
from main.models.job import Job
from main.models.transportation_method import TransportationMethod


class AttendanceProfile(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    user = models.ForeignKey(User)
    year = models.IntegerField()

    housing_group = models.ForeignKey(HousingGroup, related_name='residents', null=True, blank=True)
    transportation_method = models.ForeignKey(TransportationMethod, related_name='attendees', null=True, blank=True)

    arrival_date = models.CharField(
        max_length=16,
        choices=(
            ('wednesday1', 'Wednesday (Early)'),
            ('thursday1', 'Thursday (Early)'),
            ('friday1', 'Friday (Early)'),
            ('saturday', 'Saturday (Early)'),
            ('sunday', 'Sunday'),
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday2', 'Wednesday'),
            ('thursday2', 'Thursday'),
            ('friday2', 'Friday'),
        ),
        blank=True,
        null=True
    )
    departure_date = models.CharField(
        max_length=16,
        choices=(
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday (Man Burn)'),
            ('sunday', 'Sunday (Temple Burn)'),
            ('monday', 'Monday (Late Crew)'),
            ('tuesday', 'Tuesday (Late Crew)'),
        ),
        blank=True,
        null=True
    )

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


class AttendanceProfileForm(ModelForm):
    class Meta:
        model = AttendanceProfile
        fields = [
            'arrival_date',
            'departure_date',
            'transportation_method',
            'has_early_pass',
            'has_ticket',
            'has_vehicle_pass',
            'bicycle_status',
            'job_preferences',
            'shift_time_preference',
            'shift_day_preference',
        ]

        labels = {
            'arrival_date': 'What day do you plan to arrive?',
            'departure_date': 'What day do you plan to leave?',
            'transportation_method': 'How are you planning on getting there?',
            'has_early_pass': 'Do you have any early passes?',
            'has_ticket': 'Do you have any tickets yet?',
            'has_vehicle_pass': 'Do you have a vehicle pass?',
            'bicycle_status': 'What\'s your bicycle plan?',
            'job_preferences': 'Are there specific on-playa jobs you\'re interested in?',
            'shift_time_preference': 'Do you prefer daytime or evening shifts?',
            'shift_day_preference': 'How would you like to spread your shifts?',
        }

        widgets = {
            'job_preferences': CheckboxSelectMultiple(),
        }