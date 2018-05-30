import os

from django.test import TestCase

from main.views.signup import SignUpForm


class TestSignupView(TestCase):
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
        }
        os.environ['RECAPTCHA_TESTING'] = 'True'
        form = SignUpForm(data)
        self.assertTrue(form.is_valid())
