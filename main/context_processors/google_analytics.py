from typing import Dict
from django.http import HttpRequest
from playacamp import settings


def inject_google_analytics_tracking_id(request: HttpRequest) -> Dict[str, str]:
    return {
        'google_analytics_tracking_id': settings.GOOGLE_ANALYTICS_TRACKING_ID,
    }