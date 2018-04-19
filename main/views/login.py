from django.contrib.auth import authenticate, login


def submit(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if user.profile:
            return redirect(user.profile)
        return HttpResponse('OK')
    else:
        return HttpResponse("Invalid credentials.", status_code=400)

