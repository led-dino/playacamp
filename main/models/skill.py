from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django_resized import ResizedImageField


class Skill(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    picture = ResizedImageField(size=[256, 256], quality=100, upload_to='skill_pictures', null=True, blank=True)

    def __str__(self):
        # type: () -> str
        return self.name

    def picture_url(self):
        # type: () -> Optional[str]
        if self.picture:
            return self.picture.url
        return static('default-merit-badge.jpg')
