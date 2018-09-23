from typing import Type

from django.db import models
from django.contrib.auth.models import User
from django.db.models import QuerySet, Count, F



class Team(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    members = models.ManyToManyField(User, blank=True, related_name='teams', through='TeamMembership')
    max_size = models.IntegerField(blank=False, null=False, default=1)
    is_early_crew = models.BooleanField(default=False)
    is_late_crew = models.BooleanField(default=False)

    @property
    def leads(self):
        return self.members.filter(memberships__is_lead=True).all()

    @property
    def non_leads(self):
        return self.members.filter(memberships__is_lead=False).all()

    @property
    def is_full(self) -> bool:
        return len(self.members.all()) >= self.max_size

    def ensure_membership(self, user: User, member: bool) -> bool:
        """
        Ensure that a `User` if on or off this `Team`.

        :param user: The `User` to add or remove from the `Team`
        :param member: `bool` which determines whether the `User` should be on or off the `Team`.
        :return: `True` if successfully ensured, `False` otherwise (e.g. if `member == True` but
            the `Team` was full).
        """
        user_team = user.teams.filter(pk=self.pk).first()
        is_on_team = user_team is not None
        if is_on_team == member:
            return True
        return self.toggle_membership(user)

    def toggle_membership(self, user: User) -> bool:
        """Toggles the membership of a `User` for this `Team`.

        :param user: The `User` to toggle.
        :return: `True` if the `User`'s membership was successfully toggled,
            `False` otherwise (e.g. if the `Team` is full)
        """
        try:
            my_team = user.teams.get(pk=self.id)
        except Team.DoesNotExist:
            my_team = None

        if my_team is not None:
            user.memberships.filter(team__id=self.id).delete()
            return True

        if self.is_full:
            return False

        from main.models import TeamMembership
        membership = TeamMembership()
        membership.member = user
        membership.team = self
        membership.save()
        return True

    @classmethod
    def objects_ordered_by_remaining_space(cls) -> QuerySet:
        return cls.objects\
            .annotate(num_members=Count('members'),
                      needed_members=F('num_members')-F('max_size'))\
            .order_by(F('needed_members'))

    def __str__(self):
        return '{} ({}/{})'.format(self.name, self.members.count(), self.max_size)

