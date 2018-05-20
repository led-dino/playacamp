from django.contrib.auth.views import login
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect


def get(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('user-profile-me')
    return login(request)