import os
from typing import Dict

import boto3
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse
from moto import mock_s3
from moto import mock_s3_deprecated as mock_s3_b2

from main.models import UserProfile, FoodRestriction, Skill
from playacamp import settings


def get_absolute_url_from_relative(relative_url: str) -> str:
    fake_request = RequestFactory().post('/foobar', follow=True, secure=True)
    return fake_request.build_absolute_uri(relative_url)


class TestUserProfileView(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='foobar',
                                        email='foobar@gmail.com',
                                        password='foobarbaz')
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.save()

        user2 = User.objects.create_user(username='bazqux',
                                         email='bazqux@gmail.com',
                                         password='foobarbaz')
        user_profile2 = UserProfile()
        user_profile2.user = user2
        user_profile2.save()

        self.user_profile = user_profile
        self.user_profile2 = user_profile2


class TestUserProfileGetView(TestUserProfileView):
    def test_get_me(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.get(reverse('user-profile-me'), secure=True)
        self.assertEqual(response.status_code, 200)

    def test_get_other_unverified(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')
        self.user_profile.is_verified_by_admin = False
        self.user_profile.save()

        response = self.client.get(reverse('user-profile', args=[self.user_profile2.user.id]), secure=True)
        self.assertEqual(response.status_code, 403)

    def test_get_other_verified(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')
        self.user_profile.is_verified_by_admin = True
        self.user_profile.save()

        response = self.client.get(reverse('user-profile', args=[self.user_profile2.user.id]), secure=True)
        self.assertEqual(response.status_code, 200)


class TestUserProfileUpdateBasicsView(TestUserProfileView):
    def build_basics_data(self, **kwargs) -> Dict[str, str]:
        data = {
            'playa_name': '',
            'zipcode': '',
            'social_link_fb': '',
            'social_link_twitter': '',
            'phone': '',
            'years_on_playa': '',
            'bio': '',
        }
        data.update(kwargs)
        return data

    def test_update_basics_empty(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_zipcode(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(zipcode='94103'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_invalid_zipcode(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(zipcode='9410'),
                                    secure=True)
        self.assertEqual(response.status_code, 400)

    def test_update_phone(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(phone='555-555-5555'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.phone_number, '555-555-5555')

    def test_update_invalid_phone(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(phone='555-5555'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 400)

    def test_update_years_on_playa(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(years_on_playa='5'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)

    def test_update_invalid_years_on_playa(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(years_on_playa='foo'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 400)

    def test_update_social_links(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(social_link_fb='https://foobar.com'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        social_media_links = list(self.user_profile.social_media_links.all())
        self.assertEqual(len(social_media_links), 1)
        self.assertEqual(social_media_links[0].account_type, 'fb')
        self.assertEqual(social_media_links[0].link, 'https://foobar.com')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(social_link_twitter='https://foobar.com'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        social_media_links = list(self.user_profile.social_media_links.all())
        self.assertEqual(len(social_media_links), 2)
        self.assertEqual({l.account_type for l in social_media_links}, {'fb', 'twitter'})
        self.assertEqual({l.link for l in social_media_links}, {'', 'https://foobar.com'})

    def test_update_playa_name(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(playa_name='Foobar'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.playa_name, 'Foobar')

    def test_update_bio(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('update-basics-submit'),
                                    data=self.build_basics_data(bio='Hey there'),
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.biography, 'Hey there')


class TestUserProfileChangeAttendingView(TestUserProfileView):
    def test_change_attending_view(self) -> None:
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


class TestUpdatedSkillsView(TestUserProfileView):
    def setUp(self) -> None:
        super(TestUpdatedSkillsView, self).setUp()

        self.heavy_lifting = Skill()
        self.heavy_lifting.save()

        self.coding = Skill()
        self.coding.save()

    def test_updated_skills_empty(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('updated-skills'),
                                    data={},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(len(self.user_profile.skills.all()), 0)

    def test_updated_skills_add_remove(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('updated-skills'),
                                    data={'skills[]': [self.heavy_lifting.id, self.coding.id]},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual({s.id for s in self.user_profile.skills.all()},
                         {self.heavy_lifting.id, self.coding.id})

        response = self.client.post(reverse('updated-skills'),
                                    data={'skills[]': [self.heavy_lifting.id]},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual({s.id for s in self.user_profile.skills.all()},
                         {self.heavy_lifting.id})

        response = self.client.post(reverse('updated-skills'),
                                    data={'skills[]': []},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual({s.id for s in self.user_profile.skills.all()}, set())


class TestUpdatedFoodRestrictionsView(TestUserProfileView):
    def setUp(self) -> None:
        super(TestUpdatedFoodRestrictionsView, self).setUp()

        self.vegetarian = FoodRestriction(name='Vegetarian')
        self.vegetarian.save()

        self.vegan = FoodRestriction(name='Vegan')
        self.vegan.save()

    def test_updated_empty(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('updated-food-restrictions'),
                                    data={},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual(len(self.user_profile.food_restrictions.all()), 0)

    def test_updated_add_remove(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.post(reverse('updated-food-restrictions'),
                                    data={'food_restrictions[]': [self.vegan.id, self.vegetarian.id]},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual({fr.id for fr in self.user_profile.food_restrictions.all()},
                         {self.vegan.id, self.vegetarian.id})

        response = self.client.post(reverse('updated-food-restrictions'),
                                    data={'food_restrictions[]': [self.vegan.id]},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual({fr.id for fr in self.user_profile.food_restrictions.all()},
                         {self.vegan.id})

        response = self.client.post(reverse('updated-food-restrictions'),
                                    data={'food_restrictions[]': []},
                                    secure=True,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.user_profile.refresh_from_db()
        self.assertEqual({fr.id for fr in self.user_profile.food_restrictions.all()}, set())


class TestUpdateProfilePictureView(TestUserProfileView):
    def setUp(self) -> None:
        self.mock_s3 = mock_s3()
        self.mock_s3.start()
        self.mock_s3_b2 = mock_s3_b2()
        self.mock_s3_b2.start()

        # Setup the appropriate buckets
        self.s3_conn = boto3.resource('s3', region_name='us-west-2')
        self.s3_conn.create_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
        super(TestUpdateProfilePictureView, self).setUp()

    def tearDown(self) -> None:
        super(TestUpdateProfilePictureView, self).tearDown()
        self.mock_s3.stop()

    def test_get_and_submit_profile_picture_form(self) -> None:
        self.client.login(username='foobar', password='foobarbaz')

        response = self.client.get(reverse('profile-pic-form'), secure=True)
        self.assertEqual(response.status_code, 200)

        with open(os.path.join(settings.STATIC_ROOT, 'default-profile-pic.png'), 'rb') as f:
            photo = SimpleUploadedFile('photo.png', f.read(), 'image/png')
            response = self.client.post(reverse('profile-pic-form-submit'),
                                        data={'file': photo},
                                        secure=True,
                                        follow=True)
        self.assertEqual(response.status_code, 200)
        bucket = self.s3_conn.Bucket(settings.AWS_STORAGE_BUCKET_NAME)
        objects = list(bucket.objects.all())
        self.assertEqual(len(objects), 1)
        self.assertEqual(objects[0].key,
                         os.path.join(settings.MEDIAFILES_LOCATION,
                                      'profile_pictures',
                                      'photo.png'))
