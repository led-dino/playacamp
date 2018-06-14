from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required
def dues(request: HttpRequest) -> HttpResponse:
    return render(request, 'static/dues.html', {
        'profile': request.user.profile,
    })


@login_required
def newbies(request: HttpRequest) -> HttpResponse:
    return render(request, 'static/newbies.html', {
        'profile': request.user.profile,
        'confetti_count': range(150)
    })
