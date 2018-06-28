from django.test import TestCase

from main.models import HousingGroup


class AttendanceProfileTest(TestCase):
    def test_housing_types(self):
        for value, verbose in HousingGroup.HOUSING_CHOICES:
            housing_group = HousingGroup(housing_type=value)
            housing_group.full_clean()
            housing_group.save()
