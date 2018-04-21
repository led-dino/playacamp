import sys

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from main.models.attendance_profile import AttendanceProfile, AttendanceProfileForm


@login_required
def get(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = User.objects.get(pk=user_id)

    current_year = timezone.now().year
    try:
        attendance = AttendanceProfile.objects.get(user=user,
                                                   year=current_year,
                                                   deleted_at=None)
        attendance_form = AttendanceProfileForm(instance=attendance)
    except AttendanceProfile.DoesNotExist:
        attendance_form = AttendanceProfileForm() if request.user.id == user.id else None

    return render(request, 'user_profile/view.html', context={
        'profile': user.profile,
        'is_editable': request.user.id == user.id,
        'attendance_form': attendance_form,
        'messages': messages.get_messages(request),
    })


@login_required
def changed_attending(request):
    if request.method != 'POST':
        raise Http404

    is_attending = request.POST.get('is-attending') == 'on'
    current_year = timezone.now().year

    try:
        attendance = AttendanceProfile.objects.get(user=request.user,
                                                   year=current_year)
    except AttendanceProfile.DoesNotExist:
        attendance = None

    if is_attending:
        if attendance is None:
            return create_attendance_record(request, current_year)

        if attendance.deleted_at is not None:
            attendance.deleted_at = None
            attendance.save()
            return redirect(get)

        return update_attendance_record(request, attendance)
    else:
        if attendance is not None and attendance.deleted_at is None:
            return delete_attendance_record(request, attendance)
        return redirect(get)


def create_attendance_record(request, year):
    assert request.user.is_authenticated
    sys.stdout.flush()

    attendance = AttendanceProfile(user=request.user, year=year)
    attendance.save()
    return redirect(get)


def delete_attendance_record(request, attendance):
    assert request.user.is_authenticated
    sys.stdout.flush()

    attendance.deleted_at = timezone.now()
    attendance.save()

    return redirect(get)


def update_attendance_record(request, attendance):
    assert request.user.is_authenticated
    sys.stdout.flush()

    form = AttendanceProfileForm(request.POST, instance=attendance)
    if form.is_valid():
        form.save()
    else:
        for error in form.errors:
            messages.add_message(request, messages.ERROR, form.errors[error][0])

    return redirect(get)
