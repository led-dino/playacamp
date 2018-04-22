from django.db import models
from django.contrib.auth.models import User
from main.models.team import Team


class TeamMembership(models.Model):
    team = models.ForeignKey(Team)
    member = models.ForeignKey(User, related_name='memberships')
    is_lead = models.BooleanField(default=False)

    def __str__(self):
        return '<{}, {}>'.format(self.team, self.member)


