from typing import Optional, List

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django.utils import timezone
from django_resized import ResizedImageField

import datetime
import pytz
import phonenumbers
from uszipcode import ZipcodeSearchEngine
from timezonefinder import TimezoneFinder
from uszipcode.searchengine import Zipcode

from main.models import AttendanceProfile
from main.models.food_restriction import FoodRestriction
from main.models.skill import Skill
from playacamp import settings


def requires_verified_by_admin(func):
    def check_verified_by_admin(user):
        if not user.is_authenticated:
            return False
        if user.profile.is_verified_by_admin:
            return True
        raise PermissionDenied('You need to be verified by an admin.')
    decorator = user_passes_test(check_verified_by_admin)
    return decorator(func)


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    profile_picture = ResizedImageField(size=[512, 512], quality=100, upload_to='profile_pictures', null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    biography = models.TextField(blank=True)
    playa_name = models.CharField(max_length=64, blank=True, null=True)
    food_restrictions = models.ManyToManyField(FoodRestriction, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    years_on_playa = models.IntegerField(blank=True, null=True)
    invited_by = models.CharField(max_length=64, null=True, blank=True)
    is_verified_by_admin = models.NullBooleanField()

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def first_name(self) -> str:
        return self.user.first_name

    @property
    def last_name(self) -> str:
        return self.user.last_name

    @property
    def email(self) -> str:
        return self.user.email

    def try_fetch_current_attendance(self) -> Optional[AttendanceProfile]:
        current_year = timezone.now().year
        try:
            return AttendanceProfile.objects.get(user=self.user,
                                                 year=current_year)
        except AttendanceProfile.DoesNotExist:
            return None

    @property
    def is_attending(self) -> bool:
        return self.try_fetch_current_attendance() is not None

    def profile_pic_url(self) -> str:
        if self.profile_picture:
            assert settings.AWS_STORAGE_BUCKET_NAME
            return self.profile_picture.url
        return static('default-profile-pic.png')

    def get_rich_zipcode(self) -> Optional[Zipcode]:
        if not self.zipcode:
            return None
        search = ZipcodeSearchEngine()
        return search.by_zipcode(self.zipcode)

    def city_and_state(self) -> Optional[str]:
        zipcode = self.get_rich_zipcode()
        if zipcode is None:
            return None
        return '{}, {}'.format(zipcode['City'], zipcode['State'])

    def get_timezone_offset(self) -> Optional[str]:
        zipcode = self.get_rich_zipcode()
        if zipcode is None:
            return None
        tf = TimezoneFinder()
        longitude = zipcode['Longitude']
        latitude = zipcode['Latitude']
        timezone_name = tf.timezone_at(lng=longitude, lat=latitude)
        if timezone_name is None:
            return None
        return datetime.datetime.now(pytz.timezone(timezone_name)).strftime('%z')

    def missing_social_media_link_types(self) -> List[str]:
        from main.models import SocialMediaLink
        existing_links = {(link.account_type, link.get_account_type_display()) for link in self.social_media_links.all()}
        return list(set(SocialMediaLink.ACCOUNT_TYPES) - existing_links)

    def formatted_phone_number(self) -> Optional[str]:
        if self.phone_number:
            try:
                parsed_number = phonenumbers.parse(self.phone_number, 'US')
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumber())
            except Exception as e:
                import traceback
                traceback.print_exc()
                print('Error parsing phone number: {}'.format(self.phone_number))
            return None
        return None

    def get_absolute_url(self) -> str:
        return reverse('user-profile', kwargs={'user_id': self.user.id})

    def get_formatted_name(self) -> str:
        full_name = self.user.get_full_name()
        base_name = full_name if full_name else self.user.get_username()
        if self.playa_name:
            return '{} ({})'.format(base_name, self.playa_name)
        return full_name

    def __str__(self) -> str:
        return str(self.user)

    @classmethod
    def parse_phone_number(cls, raw_number: str) -> str:
        try:
            parsed_number = phonenumbers.parse(raw_number, 'US')
            formatted_phone = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumber())
            if len(formatted_phone) != 12:
                raise ValidationError('Invalid phone number. Expected xxx-xxx-xxxx')
            chunks = formatted_phone.split('-')
            if len(chunks) != 3 or len(chunks[0]) != 3 or len(chunks[1]) != 3 or len(chunks[2]) != 4:
                raise ValidationError('Invalid phone number. Expected xxx-xxx-xxxx')
        except Exception:
            raise ValidationError('Invalid phone number. Expected xxx-xxx-xxxx')
        return formatted_phone

    @classmethod
    def csv_columns(cls) -> List[str]:
        return [
            "First Name",
            "Last Name",
            "Email",
            "Attending",
            "Location",
        ]

    def to_csv(self) -> List[str]:
        attendance = self.try_fetch_current_attendance()
        return [
            self.first_name,
            self.last_name,
            self.email,
            attendance is not None,
            self.city_and_state(),
        ]