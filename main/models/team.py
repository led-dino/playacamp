from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    members = models.ManyToManyField(User, blank=True, related_name='teams', through='TeamMembership')
    max_size = models.IntegerField(blank=False, null=False, default=1)

    @property
    def leads(self):
        return self.members.filter(memberships__is_lead=True).all()

    @property
    def non_leads(self):
        return self.members.filter(memberships__is_lead=False).all()

    @property
    def is_full(self) -> bool:
        return len(self.members.all()) >= self.max_size

    def __str__(self):
        return self.name

