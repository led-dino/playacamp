from django.db import models
from django.contrib.auth.models import User
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.urls import reverse
from django_resized import ResizedImageField

import datetime
import pytz
import phonenumbers
from uszipcode import ZipcodeSearchEngine
from timezonefinder import TimezoneFinder
from main.models.food_restriction import FoodRestriction
from main.models.skill import Skill


class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile')
    profile_picture = ResizedImageField(size=[512, 512], quality=100, upload_to='profile_pictures', null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    zipcode = models.CharField(max_length=5, null=True, blank=True)
    biography = models.TextField(blank=True)
    playa_name = models.CharField(max_length=64, blank=True, null=True)
    food_restrictions = models.ManyToManyField(FoodRestriction, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    years_on_playa = models.IntegerField(blank=True, null=True)

    def profile_pic_url(self):
        # type: () -> str
        if self.profile_picture:
            return self.profile_picture.url
        return static('default-profile-pic.png')

    def get_rich_zipcode(self):
        if not self.zipcode:
            return None
        search = ZipcodeSearchEngine()
        return search.by_zipcode(self.zipcode)

    def get_city_and_state(self):
        # type: () -> Optional[str]
        zipcode = self.get_rich_zipcode()
        if zipcode is None:
            return None
        return '{}, {}'.format(zipcode['City'], zipcode['State'])

    def get_timezone_offset(self):
        # type: () -> Optional[str]
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

    def formatted_phone_number(self):
        # type: () -> Optional[str]
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

    def get_absolute_url(self):
        return reverse('user-profile', kwargs={'user_id': self.user.id})

    def __str__(self):
        # type: () -> str
        return str(self.user)
