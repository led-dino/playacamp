from django.contrib.auth.models import User
from django.test import TestCase

from main.models import UserProfile, FoodRestriction


class UserProfileTest(TestCase):
    def test_details(self):
        alice = User.objects.create_user('alice', 'alice@foobar.com', 'passwd')
        alice.save()

        profile = UserProfile(user=alice,
                              biography='Just a small-town girl...',
                              playa_name='Yoshi')
        profile.save()

        self.assertEqual(alice.profile, profile)
        self.assertEqual(set(alice.profile.food_restrictions.all()), set())

        vegan = FoodRestriction(name='Vegan', description='No animal products.')
        vegan.save()

        alice.profile.food_restrictions.add(vegan)
        alice.save()

        self.assertEqual(set(alice.profile.food_restrictions.all()), {vegan})

    def test_phone_number_parsing(self):
        alice = User.objects.create_user('alice', 'alice@foobar.com', 'passwd')
        alice.save()

        profile = UserProfile(user=alice,
                              biography='Just a small-town girl...',
                              playa_name='Yoshi')
        profile.save()

        test_cases = [
            '5555555555',
            '555-555-5555',
            '15555555555',
            '1-555-555-5555',
            '+15555555555',
            '+1-555-555-5555',
        ]

        for phone_number in test_cases:
            parsed_number = UserProfile.parse_phone_number(phone_number)
            assert len(parsed_number) == 12

        self.assertTrue(True)
