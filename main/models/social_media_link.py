from urllib.parse import urlparse

from django.db import models

from main.models.user_profile import UserProfile


class SocialMediaLink(models.Model):
    ACCOUNT_TYPES = (
        ('fb', 'Facebook'),
        ('twitter', 'Twitter'),
    )
    user_profile = models.ForeignKey(UserProfile, related_name='social_media_links')
    account_type = models.CharField(
        max_length=16,
        choices=ACCOUNT_TYPES)
    link = models.URLField(blank=False, null=False)

    def formatted_link(self) -> str:
        return ''.join(urlparse(self.link)[1:3])

    def __str__(self):
        # type: () -> str
        return 'SocialMediaLink({}, {})'.format(self.user_profile, self.account_type)
