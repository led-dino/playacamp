import phonenumbers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseBadRequest, HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from main.models import UserProfile


def get(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('user-profile-me')
    return render(request, 'registration/signup.html')


def post(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return redirect('signup')

    first_name = str(request.POST['first-name'])
    if first_name == '':
        return HttpResponseBadRequest('First name required!')

    last_name = str(request.POST['last-name'])
    if last_name == '':
        return HttpResponseBadRequest('Last name required!')

    password = str(request.POST['password'])
    if len(password) < 8:
        return HttpResponseBadRequest('Password must be at least 8 characters!')

    duplicate_password = str(request.POST['duplicate-password'])
    if password != duplicate_password:
        return HttpResponseBadRequest("Passwords don't match!")

    try:
        years_on_playa = int(request.POST['years-on-playa'])
    except ValueError:
        return HttpResponseBadRequest('Need a number for years on playa!')

    email = str(request.POST['email'])
    if email == '':
        return HttpResponseBadRequest("Email is required!")

    phone = str(request.POST['phone'])
    parsed_number = phonenumbers.parse(phone, 'US')
    formatted_phone = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumber())

    zipcode = str(request.POST['zipcode'])
    if len(zipcode) != 5:
        return HttpResponseBadRequest("Zipcode looks invalid!")

    try:
        User.objects.create_user(username=email,
                                 email=email,
                                 password=password,
                                 first_name=first_name,
                                 last_name=last_name)
    except IntegrityError as e:
        if str(e) == 'UNIQUE constraint failed: auth_user.username':
            return HttpResponseBadRequest('User already exists.')
        raise

    user = authenticate(username=email, password=password)
    assert user is not None

    user_profile = UserProfile()
    user_profile.years_on_playa = years_on_playa
    user_profile.phone_number = formatted_phone
    user_profile.zipcode = zipcode
    user_profile.user = user
    user_profile.save()

    return redirect(user_profile)
