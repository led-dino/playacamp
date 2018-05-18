from django.shortcuts import render, redirect


def get(request):
    if request.user.is_authenticated:
        return redirect('user-profile-list')
    return render(request, 'index.html')
