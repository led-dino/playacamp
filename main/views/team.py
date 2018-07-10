from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect

from main.models import Team, TeamMembership


@login_required
def get(request: HttpRequest, team_id: int) -> HttpResponse:
    is_allowed_to_view_members = request.user.profile.is_verified_by_admin
    team = Team.objects.get(pk=team_id)
    try:
        my_team = request.user.teams.filter(pk=team_id).first()
    except Team.DoesNotExist:
        my_team = None

    is_member = my_team is not None

    return render(request, 'team/detail.html', context={
        'profile': request.user.profile,
        'team': team,
        'is_member': is_member,
        'is_allowed_to_view_members': is_allowed_to_view_members,
    })


@login_required
def list(request: HttpRequest) -> HttpResponse:
    teams = Team.objects.all()
    my_team_ids = [team.id for team in request.user.teams.all()]
    return render(request, 'team/list.html', context={
        'profile': request.user.profile,
        'my_team_ids': my_team_ids,
        'teams': teams,
    })


@login_required
def toggle_membership(request: HttpRequest, team_id: int) -> HttpResponse:
    if request.method != 'POST':
        raise Http404

    next_url = request.POST.get('next')
    team = Team.objects.get(pk=team_id)
    successfully_toggled = team.toggle_membership(request.user)
    if not successfully_toggled:
        return HttpResponseBadRequest('Sorry, {} team is full.'.format(team.name))

    if next_url:
        return redirect(next_url)
    return redirect(get, team_id)
