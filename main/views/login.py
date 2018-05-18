from django.contrib.auth.views import login
from django.shortcuts import redirect


def get(request):
    if request.user.is_authenticated:
        return redirect('user-profile-me')
    return login(request)