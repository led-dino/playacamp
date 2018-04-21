import datetime

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from main.models.attendance_profile import AttendanceProfile


@login_required
def get(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = User.objects.get(pk=user_id)

    current_year = datetime.datetime.utcnow().year
    try:
        attendance = AttendanceProfile.objects.get(year=current_year)
    except AttendanceProfile.DoesNotExist:
        attendance = None

    return render(request, 'user_profile/view.html', context={
        'profile': user.profile,
        'attendance': attendance,
    })


@login_required
def change_attending(request):
    if request.method != 'POST':
        raise Http404
    return redirect(get)


@login_required
def submit_attending(request):
    if request.method != 'POST':
        raise Http404
    return redirect(get)
