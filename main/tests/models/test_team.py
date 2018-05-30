from django.contrib.auth.models import User
from django.test import TestCase

from main.models import Team, TeamMembership


class TeamTest(TestCase):
    def test_details(self):
        team = Team(name='Test Team',
                    description='This is a test.')
        team.save()

        alice = User.objects.create_user('alice', 'alice@foobar.com', 'passwd')
        alice.save()

        bob = User.objects.create_user('bob', 'bob@foobar.com', 'passwd')
        bob.save()

        alice_membership = TeamMembership(team=team, member=alice, is_lead=True)
        alice_membership.save()

        bob_membership = TeamMembership(team=team, member=bob)
        bob_membership.save()

        self.assertEqual(set(team.members.all()), {alice, bob})
        self.assertEqual(list(team.leads), [alice])
