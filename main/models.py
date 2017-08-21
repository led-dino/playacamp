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


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    biography = models.TextField(blank=True)
    playa_name = models.CharField(max_length=64, blank=True, null=True)
    food_restrictions = models.ManyToManyField(FoodRestriction)
