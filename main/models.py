from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    members = models.ManyToManyField(User, blank=True, through='TeamMembership')

    @property
    def leads(self):
        return self.members.filter(teammembership__is_lead=True).all()

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    team = models.ForeignKey(Team)
    member = models.ForeignKey(User)
    is_lead = models.BooleanField(default=False)

    def __str__(self):
        return '<{}, {}>'.format(self.team, self.member)


class FoodRestriction(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    biography = models.TextField(blank=True)
    playa_name = models.CharField(max_length=64, blank=True, null=True)
    food_restrictions = models.ManyToManyField(FoodRestriction, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    years_on_playa = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user)


class HousingGroup(models.Model):
    CAMP_YURT = ('campyurt', 'Camp Yurt')
    NEW_YURT = ('newyurt', 'New Yurt')
    TENT = ('tent', 'Tent')
    RECREATIONAL_VEHICLE = ('rv', 'RV')
    CONTAINER = ('container', 'Container')
    OTHER = ('other', 'Other')
    HOUSING_CHOICES = (CAMP_YURT, NEW_YURT, TENT, RECREATIONAL_VEHICLE, CONTAINER, OTHER)

    housing_type = models.CharField(
        max_length=10,
        choices=HOUSING_CHOICES,
        blank=True,
        null=True
    )

    def __str__(self):
        return 'HousingGroup #{}: {}'.format(self.id, self.housing_type)


class TransportationMethod(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class Job(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name


class JobAssignment(models.Model):
    job = models.ForeignKey(Job)
    attendee = models.ForeignKey('AttendanceProfile', related_name='job_assignments')
    date = models.DateField()

    def __str__(self):
        return 'JobAssignment: ({}, {})'.format(self.job, self.attendee)


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
