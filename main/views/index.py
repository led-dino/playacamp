from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


def get(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return render(request, 'index.html')

    if request.user.profile.is_verified_by_admin:
        return redirect('user-profile-list')
    return redirect('user-profile-me')
