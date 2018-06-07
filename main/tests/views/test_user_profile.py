from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse

from main.models import UserProfile


def get_absolute_url_from_relative(relative_url: str) -> str:
    fake_request = RequestFactory().post('/foobar', follow=True, secure=True)
    return fake_request.build_absolute_uri(relative_url)


class TestUserProfileViews(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='foobar',
                                        email='foobar@gmail.com',
                                        password='foobarbaz')
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()
        self.user_profile = user_profile

    def test_change_attending_view(self):
        self.client.login(username='foobar', password='foobarbaz')
        expected_redirect_url = get_absolute_url_from_relative(reverse('user-profile-me'))
        response = self.client.post(reverse('changed-attending'), {
            'is-attending': 'on',
        }, follow=True, secure=True)
        self.assertRedirects(response, expected_redirect_url)
        attendance = self.user_profile.try_fetch_current_attendance()
        self.assertIsNotNone(attendance)
        self.assertFalse(attendance.deleted_at)

        response = self.client.post(reverse('changed-attending'), {
            'is-attending': 'off',
        }, follow=True, secure=True)
        self.assertRedirects(response, expected_redirect_url)
        attendance = self.user_profile.try_fetch_current_attendance()
        self.assertTrue(attendance.deleted_at)
