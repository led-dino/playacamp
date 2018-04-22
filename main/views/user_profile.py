import sys

from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from main.models import Skill, FoodRestriction
from main.models.attendance_profile import AttendanceProfile, AttendanceProfileForm


@login_required
def get(request, user_id=None):
    user = request.user if user_id is None else User.objects.get(pk=user_id)
    is_editable = request.user.id == user.id

    current_year = timezone.now().year
    try:
        attendance = AttendanceProfile.objects.get(user=user,
                                                   year=current_year,
                                                   deleted_at=None)
        attendance_form = AttendanceProfileForm(instance=attendance)
    except AttendanceProfile.DoesNotExist:
        # There exists no AttendanceProfile already, so if the page isn't
        # editable we don't want to display a form.
        attendance_form = AttendanceProfileForm() if is_editable else None

    all_skills_by_name = {s.name: s for s in Skill.objects.all()}
    my_skills_by_name = {s.name: s for s in user.profile.skills.all()}
    other_skills_by_name = {}
    for skill_name in all_skills_by_name:
        if skill_name in my_skills_by_name:
            continue
        other_skills_by_name[skill_name] = all_skills_by_name[skill_name]

    all_food_restrictions_by_name = {fr.name: fr for fr in FoodRestriction.objects.all()}
    my_food_restrictions_by_name = {fr.name: fr for fr in user.profile.food_restrictions.all()}
    other_food_restrictions_by_name = {}
    for fr_name in all_food_restrictions_by_name:
        if fr_name in my_food_restrictions_by_name:
            continue
        other_food_restrictions_by_name[fr_name] = all_food_restrictions_by_name[fr_name]

    return render(request, 'user_profile/view.html', context={
        'profile': user.profile,
        'is_editable': is_editable,
        'attendance_form': attendance_form,
        'messages': messages.get_messages(request),
        'other_skills': other_skills_by_name.values(),
        'other_food_restrictions': other_food_restrictions_by_name.values(),
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


@login_required
def updated_skills(request):
    if request.method != 'POST':
        raise Http404

    profile = request.user.profile
    current_skill_ids = {int(skill_id) for skill_id in request.POST.getlist('skills[]', [])}
    all_skills = Skill.objects.all()

    profile.skills.set([s for s in all_skills if s.id in current_skill_ids])
    profile.save()

    return redirect(get)


@login_required
def updated_food_restrictions(request):
    if request.method != 'POST':
        raise Http404

    profile = request.user.profile
    current_restriction_ids = {int(rid) for rid in request.POST.getlist('food_restrictions[]', [])}
    all_food_restrictions = FoodRestriction.objects.all()

    profile.food_restrictions.set([fr for fr in all_food_restrictions if fr.id in current_restriction_ids])
    profile.save()

    return redirect(get)