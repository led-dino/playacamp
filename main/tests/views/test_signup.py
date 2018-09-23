import os

from django.contrib.auth.models import User
from django.test import TestCase

from main.models import Team, UserProfile, TeamMembership
from main.views.signup import SignUpForm


class TestSignupView(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='foobar',
                                             email='foobar@gmail.com',
                                             password='foobarbaz')
        self.user_profile = UserProfile()
        self.user_profile.user = self.user
        self.user_profile.save()

        self.team = Team(name='Kitchen', description='Cook stuff.', max_size=2)
        self.team.save()

        self.membership = TeamMembership(team=self.team,
                                         member=self.user)
        self.membership.save()

    def test_signup_form_validation(self):
        data = {
            'first_name': 'Foo',
            'last_name': 'Bar',
            'years_on_playa': 2,
            'invited_by': 'Baz Qux',
            'email': 'foobar@gmail.com',
            'password': 'foobarbaz',
            'duplicate_password': 'foobarbaz',
            'phone': '555-555-5555',
            'zipcode': '12345',
            'g-recaptcha-response': 'PASSED',
            'interested_teams': [self.team.id],
        }
        os.environ['RECAPTCHA_TESTING'] = 'True'
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
