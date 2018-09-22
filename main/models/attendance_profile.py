from datetime import datetime, timezone, timedelta
from typing import List, Optional

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

    housing_type_preference = models.CharField(
        max_length=HousingGroup.HOUSING_TYPE_LENGTH,
        choices=HousingGroup.HOUSING_CHOICES,
        blank=True,
        null=True
    )
    housing_group = models.ForeignKey(HousingGroup, related_name='residents', null=True, blank=True)
    to_transportation_method = models.ForeignKey(TransportationMethod,
                                                 related_name='to_attendees',
                                                 null=True,
                                                 blank=True)
    from_transportation_method = models.ForeignKey(TransportationMethod,
                                                   related_name='from_attendees',
                                                   null=True,
                                                   blank=True)

    EARLY_ARRIVAL_CHOICES = (
        ('wednesday1', 'Wednesday (Early)'),
        ('thursday1', 'Thursday (Early)'),
        ('friday1', 'Friday (Early)'),
        ('saturday', 'Saturday (Early)'),
    )
    ARRIVAL_CHOICES = EARLY_ARRIVAL_CHOICES + (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday2', 'Wednesday'),
        ('thursday2', 'Thursday'),
        ('friday2', 'Friday'),
    )
    arrival_date = models.CharField(
        max_length=16,
        choices=ARRIVAL_CHOICES,
        blank=True,
        null=True
    )

    LATE_DEPARTURE_CHOICES = (
        ('monday', 'Monday (Late Crew)'),
        ('tuesday', 'Tuesday (Late Crew)'),
    )
    DEPARTURE_CHOICES = (
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday (Man Burn)'),
        ('sunday', 'Sunday (Temple Burn)'),
    ) + LATE_DEPARTURE_CHOICES
    departure_date = models.CharField(
        max_length=16,
        choices=DEPARTURE_CHOICES,
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

    @property
    def arrives_early(self) -> bool:
        return self.arrival_date in dict(AttendanceProfile.EARLY_ARRIVAL_CHOICES)

    @property
    def departs_late(self) -> bool:
        return self.departure_date in dict(AttendanceProfile.LATE_DEPARTURE_CHOICES)

    @property
    def pretty_arrival(self) -> Optional[str]:
        return dict(AttendanceProfile.ARRIVAL_CHOICES).get(self.arrival_date)

    @property
    def pretty_departure(self) -> Optional[str]:
        return dict(AttendanceProfile.DEPARTURE_CHOICES).get(self.departure_date)

    @property
    def pretty_housing_type_preference(self) -> Optional[str]:
        return dict(HousingGroup.HOUSING_CHOICES).get(self.housing_type_preference)

    def __str__(self) -> str:
        return '{}[{}]'.format(self.user, self.year)

    @classmethod
    def csv_columns(cls) -> List[str]:
        return [
            "First Name",
            "Last Name",
            "Email",
            "Has Early Pass",
            "Has Ticket",
            "Has Vehicle Pass",
            "Paid Dues",
            "Arrival Date",
            "Departure Date",
            "Housing Type Preference",
            "To Transporation",
            "From Transportation",
        ]

    def to_csv(self) -> List[str]:
        return [
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            'Unknown' if self.has_early_pass is None else self.has_early_pass,
            'Unknown' if self.has_ticket is None else self.has_ticket,
            'Unknown' if self.has_vehicle_pass is None else self.has_vehicle_pass,
            'Unknown' if self.paid_dues is None else self.paid_dues,
            self.pretty_arrival,
            self.pretty_departure,
            self.pretty_housing_type_preference,
            self.to_transportation_method.name,
            self.from_transportation_method.name,
        ]


class AttendanceProfileForm(ModelForm):
    class Meta:
        model = AttendanceProfile
        fields = [
            'arrival_date',
            'departure_date',
            'to_transportation_method',
            'from_transportation_method',
            'has_early_pass',
            'has_ticket',
            'has_vehicle_pass',
            'housing_type_preference',
            'bicycle_status',
            'job_preferences',
            'shift_time_preference',
            'shift_day_preference',
        ]

        labels = {
            'arrival_date': 'What day do you plan to arrive?',
            'departure_date': 'What day do you plan to leave?',
            'to_transportation_method': 'How are you planning on getting there?',
            'from_transportation_method': 'How are you planning on leaving?',
            'has_early_pass': 'Do you have any early passes?',
            'has_ticket': 'Do you have any tickets yet?',
            'has_vehicle_pass': 'Do you have a vehicle pass?',
            'housing_type_preference': 'Where are you planning on sleeping?',
            'bicycle_status': 'What\'s your bicycle plan?',
            'job_preferences': 'Are there specific on-playa jobs you\'re interested in?',
            'shift_time_preference': 'Do you prefer daytime or evening shifts?',
            'shift_day_preference': 'How would you like to spread your shifts?',
        }

        widgets = {
            'job_preferences': CheckboxSelectMultiple(),
        }

    def to_transportation_method_description(self) -> str:
        if self.instance is None:
            return ''
        if not self.instance.to_transportation_method:
            return ''
        return self.instance.to_transportation_method.description

    def from_transportation_method_description(self) -> str:
        if self.instance is None:
            return ''
        if not self.instance.from_transportation_method:
            return ''
        if self.instance.from_transportation_method.description == self.to_transportation_method_description():
            return ''
        return self.instance.from_transportation_method.description

    def bicycle_description(self) -> str:
        if self.instance is None:
            return ''
        if not self.instance.bicycle_status:
            return ''
        if self.instance.bicycle_status == 'rent':
            return '''Playa Bike Repair (PBR) is a great place to get your burner bike.

            Reserve your bike at https://playabikerepair.com'''
        return ''
