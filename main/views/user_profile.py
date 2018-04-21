import datetime
import sys

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from main.models.attendance_profile import AttendanceProfile, AttendanceProfileForm


@login_required
def get(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = User.objects.get(pk=user_id)

    current_year = datetime.datetime.utcnow().year
    try:
        attendance = AttendanceProfile.objects.get(year=current_year)
        attendance_form = AttendanceProfileForm(instance=attendance)
    except AttendanceProfile.DoesNotExist:
        attendance_form = AttendanceProfileForm()

    return render(request, 'user_profile/view.html', context={
        'profile': user.profile,
        'attendance_form': attendance_form,
        'messages': messages.get_messages(request),
    })


@login_required
def changed_attending(request):
    print('changed_attending')
    sys.stdout.flush()
    if request.method != 'POST':
        raise Http404

    is_attending = request.POST.get('is-attending') == 'on'
    print('is_attending = "{}"'.format(is_attending))
    sys.stdout.flush()
    current_year = datetime.datetime.utcnow().year

    try:
        attendance = AttendanceProfile.objects.get(user=request.user, year=current_year)
    except AttendanceProfile.DoesNotExist:
        attendance = None

    if is_attending and attendance is None:
        return create_attendance_record(request, current_year)

    if not is_attending and attendance is not None:
        return delete_attendance_record(request, attendance)

    return update_attendance_record(request, attendance)


def create_attendance_record(request, year):
    assert request.user.is_authenticated
    print('create attendance record')
    sys.stdout.flush()

    attendance = AttendanceProfile(user=request.user, year=year)
    attendance.save()
    return redirect(get)


def delete_attendance_record(request, attendance):
    assert request.user.is_authenticated
    print('delete attendance record')
    sys.stdout.flush()

    attendance.delete()

    return redirect(get)


def update_attendance_record(request, attendance):
    assert request.user.is_authenticated
    print('update attendance record')
    sys.stdout.flush()

    form = AttendanceProfileForm(request.POST, instance=attendance)
    if form.is_valid():
        form.save()
    else:
        for error in form.errors:
            messages.add_message(request, messages.ERROR, form.errors[error][0])

    return redirect(get)
