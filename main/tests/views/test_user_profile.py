from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import UserProfile


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
        response = self.client.post(reverse('changed-attending'), {
            'is-attending': 'on',
        })
        self.assertRedirects(response, reverse('user-profile-me'))
        attendance = self.user_profile.try_fetch_current_attendance()
        self.assertIsNotNone(attendance)
        self.assertFalse(attendance.deleted_at)

        response = self.client.post(reverse('changed-attending'), {
            'is-attending': 'off',
        })
        self.assertRedirects(response, reverse('user-profile-me'))
        attendance = self.user_profile.try_fetch_current_attendance()
        self.assertTrue(attendance.deleted_at)
