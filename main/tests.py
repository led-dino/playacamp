from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory

from .views import index
from .models import Team, TeamMembership

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/')
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        response = index(request)
        self.assertEqual(response.status_code, 200)

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
