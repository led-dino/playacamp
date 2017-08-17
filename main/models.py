from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    members = models.ManyToManyField(User, blank=True, through='TeamMembership')

    @property
    def leads(self):
        return Team.objects.all()
        #return self.members.filter(teammembership__is_lead=True).all()

    def __str__(self):
        return self.name


class TeamMembership(models.Model):
    team = models.ForeignKey(Team)
    member = models.ForeignKey(User)
    is_lead = models.BooleanField(default=False)

    def __str__(self):
        return '<{}, {}>'.format(self.team, self.member)
