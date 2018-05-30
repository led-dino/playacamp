import phonenumbers
from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest, HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from main.models import UserProfile


# We only need a small subset of the fields (along with a recaptcha)
# so this is a custom form just for the signup page.
class SignUpForm(forms.Form):
    first_name = forms.CharField(label="What is your first name little dino?", max_length=30)
    last_name = forms.CharField(label="And your last name?", max_length=30)
    years_on_playa = forms.IntegerField(label="Nice to meet you! So how many years have you gone to Burning Man?")
    invited_by = forms.CharField(label="Who invited you to LED Dinosaur?", max_length=64)
    email = forms.EmailField(label="Cool! What's your email so we can keep you up to date?")
    password = forms.CharField(label="And a password so we can identify you!",
                               widget=forms.PasswordInput,
                               min_length=8)
    duplicate_password = forms.CharField(label=" What was that password again? (in case you typo-ed)",
                                         widget=forms.PasswordInput,
                                         min_length=8)
    phone = forms.CharField(label="And your phone number por favor?")
    zipcode = forms.CharField(label="Last thing. What's your zipcode?",
                              max_length=5,
                              min_length=5)
    captcha = ReCaptchaField(label='')

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        duplicate_password = self.cleaned_data['duplicate_password']
        if password != duplicate_password:
            raise ValidationError('Passwords must match!')

    def clean_phone(self) -> str:
        return UserProfile.parse_phone_number(self.cleaned_data['phone'])


def get(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('user-profile-me')
    form = SignUpForm()
    return render(request, 'registration/signup.html', context={
        'form': form,
    })


def post(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return redirect('signup')

    form = SignUpForm(data=request.POST)
    if not form.is_valid():
        return render(request, 'registration/signup.html', context={
            'form': form,
        })

    with transaction.atomic():
        try:
            User.objects.create_user(username=form.cleaned_data['email'],
                                     email=form.cleaned_data['email'],
                                     password=form.cleaned_data['password'],
                                     first_name=form.cleaned_data['first_name'],
                                     last_name=form.cleaned_data['last_name'])
        except IntegrityError as e:
            if str(e) == 'UNIQUE constraint failed: auth_user.username':
                return HttpResponseBadRequest('User already exists.')
            raise

        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password'])
        assert user is not None

        user_profile = UserProfile()
        user_profile.years_on_playa = form.cleaned_data['years_on_playa']
        user_profile.invited_by = form.cleaned_data['invited_by']
        user_profile.phone_number = form.cleaned_data['phone']
        user_profile.zipcode = form.cleaned_data['zipcode']
        user_profile.user = user
        user_profile.save()

        login(request, user)
        return redirect(user_profile)
