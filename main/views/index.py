from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect


def get(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('user-profile-list')
    return render(request, 'index.html')
