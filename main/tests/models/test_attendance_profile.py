from django.contrib.auth.models import User
from django.test import TestCase

from main.models import HousingGroup, AttendanceProfile


class AttendanceProfileTest(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user('alice', 'alice@foobar.com', 'passwd')
        self.alice.save()

    def test_housing_types(self):
        for value, verbose in HousingGroup.HOUSING_CHOICES:
            attendance_profile = AttendanceProfile(user=self.alice,
                                                   year=2018)
            attendance_profile.full_clean()
            attendance_profile.save()
