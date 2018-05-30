import sys
from typing import Dict, Optional

import phonenumbers
from django import forms
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponseBadRequest, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

from main.models import Skill, FoodRestriction, UserProfile, SocialMediaLink
from main.models.attendance_profile import AttendanceProfile, AttendanceProfileForm
from main.models.user_profile import requires_verified_by_admin


@requires_verified_by_admin
def list_profiles(request: HttpRequest) -> HttpResponse:
    search_query = request.GET.get('search')
    if search_query is None:
        profiles = UserProfile.objects.all()
    else:
        profiles = UserProfile.objects.filter(Q(playa_name__contains=search_query) |
                                              Q(user__email__contains=search_query) |
                                              Q(user__first_name__contains=search_query) |
                                              Q(user__last_name__contains=search_query))
    return render(request, 'user_profile/list.html', context={
        'profiles': profiles,
        'search_query': search_query or '',
    })


@login_required
def get(request: HttpRequest, user_id: Optional[int]=None) -> HttpResponse:
    user = request.user if user_id is None else User.objects.get(pk=user_id)
    is_logged_in_user = request.user.id == user.id
    if not is_logged_in_user and not request.user.profile.is_verified_by_admin:
        raise PermissionDenied

    attendance = user.profile.try_fetch_current_attendance()
    if attendance:
        attendance_form = AttendanceProfileForm(instance=attendance)
    elif is_logged_in_user:
        attendance_form = AttendanceProfileForm()
    else:
        # There exists no AttendanceProfile already, so if the page isn't
        # editable we don't want to display a form.
        attendance_form = None

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
        'is_editable': is_logged_in_user,
        'attendance_form': attendance_form,
        'messages': messages.get_messages(request),
        'other_skills': other_skills_by_name.values(),
        'other_food_restrictions': other_food_restrictions_by_name.values(),
    })


@login_required
def update_basics(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        raise Http404

    profile = request.user.profile

    profile.playa_name = request.POST['playa-name']

    zipcode = request.POST['zipcode']
    if zipcode:
        if len(zipcode) != 5:
            return HttpResponseBadRequest('Invalid zipcode')
        profile.zipcode = zipcode

    links_by_account_type = {}  # type: Dict[str, str]
    for account_type, verbose_type in SocialMediaLink.ACCOUNT_TYPES:
        link = request.POST['social-link-{}'.format(account_type)]
        links_by_account_type[account_type] = link

    for social_link in profile.social_media_links.all():
        new_value = links_by_account_type[social_link.account_type]
        social_link.link = new_value
        social_link.save()
        links_by_account_type.pop(social_link.account_type)

    for account_type in links_by_account_type:
        new_link = links_by_account_type[account_type]
        if not new_link:
            continue
        social_link = SocialMediaLink()
        social_link.account_type = account_type
        social_link.link = new_link
        social_link.user_profile = profile
        social_link.save()

    phone = request.POST['phone']
    if phone:
        try:
            parsed_number = phonenumbers.parse(phone, 'US')
            profile.phone_nubmer = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumber())
        except Exception:
            return HttpResponseBadRequest('Error parsing phone number')

    years_on_playa = request.POST['years-on-playa']
    try:
        profile.years_on_playa = int(years_on_playa) if years_on_playa else ''
    except ValueError:
        return HttpResponseBadRequest('Invalid value for years on playa')

    profile.biography = request.POST['bio']
    profile.save()

    return redirect('user-profile-me')


@login_required
def changed_attending(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        raise Http404

    is_attending = request.POST.get('is-attending') == 'on'
    attendance = request.user.profile.try_fetch_current_attendance()

    if is_attending:
        if attendance is None:
            return create_attendance_record(request, timezone.now().year)

        if attendance.deleted_at is not None:
            attendance.deleted_at = None
            attendance.save()
            return redirect('user-profile-me')

        return update_attendance_record(request, attendance)
    else:
        if attendance is not None and attendance.deleted_at is None:
            return delete_attendance_record(request, attendance)
        return redirect('user-profile-me')


def create_attendance_record(request: HttpRequest, year: int) -> HttpResponse:
    assert request.user.is_authenticated
    sys.stdout.flush()

    attendance = AttendanceProfile(user=request.user, year=year)
    attendance.save()
    return redirect('user-profile-me')


def delete_attendance_record(request: HttpRequest, attendance: AttendanceProfile) -> HttpResponse:
    assert request.user.is_authenticated
    sys.stdout.flush()

    attendance.deleted_at = timezone.now()
    attendance.save()

    return redirect('user-profile-me')


def update_attendance_record(request: HttpRequest, attendance: AttendanceProfile) -> HttpResponse:
    assert request.user.is_authenticated
    sys.stdout.flush()

    form = AttendanceProfileForm(request.POST, instance=attendance)
    if form.is_valid():
        form.save()
    else:
        for error in form.errors:
            messages.add_message(request, messages.ERROR, form.errors[error][0])

    return redirect('user-profile-me')


@login_required
def updated_skills(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        raise Http404

    profile = request.user.profile
    current_skill_ids = {int(skill_id) for skill_id in request.POST.getlist('skills[]', [])}
    all_skills = Skill.objects.all()

    profile.skills.set([s for s in all_skills if s.id in current_skill_ids])
    profile.save()

    return redirect('user-profile-me')


@login_required
def updated_food_restrictions(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        raise Http404

    profile = request.user.profile
    current_restriction_ids = {int(rid) for rid in request.POST.getlist('food_restrictions[]', [])}
    all_food_restrictions = FoodRestriction.objects.all()

    profile.food_restrictions.set([fr for fr in all_food_restrictions if fr.id in current_restriction_ids])
    profile.save()

    return redirect('user-profile-me')


class UploadFileForm(forms.Form):
    file = forms.FileField()


@login_required
def get_profile_picture_form(request: HttpRequest) -> HttpResponse:
    if request.method != 'GET':
        raise Http404
    return render(request, 'user_profile/profile_pic_form.html', context={
        'photo_form': UploadFileForm(),
    })


@login_required
def submit_profile_picture_form(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        raise Http404
    print(request.FILES['file'])
    sys.stdout.flush()
    profile = request.user.profile
    profile.profile_picture = request.FILES['file']
    profile.save()
    return redirect('user-profile-me')
