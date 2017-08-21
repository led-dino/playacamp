from django.conf import settings
from storages.backends.s3boto import S3BotoStorage

class MediaStorage(S3BotoStorage):  # pylint: disable=abstract-method
    location = settings.MEDIAFILES_LOCATION
