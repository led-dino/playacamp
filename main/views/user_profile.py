from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def get(request, user_id=None):
    if user_id is None:
        user = request.user
    else:
        user = User.objects.get(pk=user_id)

    return render(request, 'user_profile/view.html', context={
        'profile': user.profile,
    })
