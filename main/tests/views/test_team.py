from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Team, UserProfile, TeamMembership


class TestTeamView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='foobar',
                                             email='foobar@gmail.com',
                                             password='foobarbaz')
        self.user_profile = UserProfile()
        self.user_profile.user = self.user
        self.user_profile.save()

        self.team = Team(name='Kitchen', description='Cook stuff')
        self.team.save()


class TestTeamGetDetailView(TestTeamView):
    def test_get(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.get(reverse('team-detail', args=[self.team.id]), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_duplicate_membership(self) -> None:
        membership1 = TeamMembership(team=self.team, member=self.user)
        membership1.save()

        membership2 = TeamMembership(team=self.team, member=self.user)
        membership2.save()

        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.get(reverse('team-detail', args=[self.team.id]), secure=True)
        self.assertEqual(response.status_code, 200)


class TestTeamListView(TestTeamView):
    def test_get(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')
        response = self.client.get(reverse('team-list'), secure=True)
        self.assertEqual(response.status_code, 200)


class TestTeamToggleMembershipView(TestTeamView):
    def test_toggle(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        self.assertEqual(len(list(self.user.teams.all())), 0)

        response = self.client.post(reverse('join-leave-team', args=[self.team.id]),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(self.user.teams.all())), 1)

        response = self.client.post(reverse('join-leave-team', args=[self.team.id]),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list(self.user.teams.all())), 0)
