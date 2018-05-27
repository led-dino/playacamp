from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from main.models import Team, TeamMembership
from main.models.user_profile import requires_verified_by_admin


@requires_verified_by_admin
def get(request: HttpRequest, team_id: int) -> HttpResponse:
    team = Team.objects.get(pk=team_id)
    try:
        my_team = request.user.teams.get(pk=team_id)
    except Team.DoesNotExist:
        my_team = None

    is_member = my_team is not None

    return render(request, 'team/detail.html', context={
        'team': team,
        'is_member': is_member,
    })


@requires_verified_by_admin
def list(request: HttpRequest) -> HttpResponse:
    teams = Team.objects.all()
    return render(request, 'team/list.html', context={
        'teams': teams,
    })


@requires_verified_by_admin
def toggle_membership(request: HttpRequest, team_id: int) -> HttpResponse:
    team = Team.objects.get(pk=team_id)
    try:
        my_team = request.user.teams.get(pk=team_id)
    except Team.DoesNotExist:
        my_team = None

    if my_team is None:
        membership = TeamMembership()
        membership.member = request.user
        membership.team = team
        membership.save()
    else:
        request.user.memberships.filter(team__id=team_id).delete()

    return redirect(get, team_id)
