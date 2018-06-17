from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import urlencode


class Notification:
    def __init__(self, name: str, current_url: str, is_dismissible: bool=False) -> None:
        self.name = name
        self.current_url = current_url
        self.is_dismissible = is_dismissible

    def dismiss_url(self) -> str:
        return reverse(dismiss_notification) + '?' + urlencode({
            'name': self.name,
            'next': self.current_url,
        })

    @classmethod
    def is_dismissed(cls, name: str, request: HttpRequest) -> bool:
        return request.session.get('notification_state_{}'.format(name)) == 'dismissed'


def dismiss_notification(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        return HttpResponseBadRequest()

    name = request.GET['name']
    next_url = request.GET['next']
    session_key = 'notification_state_{}'.format(name)
    request.session[session_key] = 'dismissed'
    return redirect(next_url)
