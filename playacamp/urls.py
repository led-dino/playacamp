from django.conf.urls import include, url
from django.contrib import admin, auth

import main.views.index
import main.views.login
import main.views.user_profile
import main.views.team
import main.views.signup

admin.autodiscover()

urlpatterns = [     # pylint: disable=invalid-name
    url(r'^$', main.views.index.get, name='index'),

    url(r'^login/$', main.views.login.get, name='login'),
    url(r'^login/password_reset/$', auth.views.password_reset, {
        'template_name': 'registration/playacamp_password_reset_form.html',
        'email_template_name': 'registration/playacamp_password_reset_email.html',
        'subject_template_name': 'registration/playacamp_password_reset_subject.txt',
    }, name='password_reset'),
    url(r'^login/password_reset/done/$', auth.views.password_reset_done, {
        'template_name': 'registration/playacamp_password_reset_done.html',
    }, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth.views.password_reset_confirm, {
        'template_name': 'registration/playacamp_password_reset_confirm.html',
    }, name='password_reset_confirm'),
    url(r'^reset/done/$', auth.views.password_reset_complete, {
        'template_name': 'registration/playacamp_password_reset_complete.html',
    }, name='password_reset_complete'),
    url(r'^logout/$', main.views.login.log_out, name='logout'),

    url(r'^signup/$', main.views.signup.get, name='signup'),
    url(r'^signup/submit/$', main.views.signup.post, name='signup-submit'),

    url(r'^teams/$', main.views.team.list, name='team-list'),
    url(r'^team/(?P<team_id>\d+)$', main.views.team.get, name='team-detail'),
    url(r'^team/(?P<team_id>\d+)/join-leave', main.views.team.toggle_membership, name='join-leave-team'),

    url(r'^profiles/$', main.views.user_profile.list_profiles, name='user-profile-list'),
    url(r'^profile/(?P<user_id>\d+)$', main.views.user_profile.get, name='user-profile'),
    url(r'^profile/me/$', main.views.user_profile.get, name='user-profile-me'),
    url(r'^profile/me/basic/$', main.views.user_profile.update_basics, name='update-basics-submit'),
    url(r'^profile/me/attendance/$', main.views.user_profile.changed_attending, name='changed-attending'),
    url(r'^profile/me/skills/$', main.views.user_profile.updated_skills, name='updated-skills'),
    url(r'^profile/me/food-restrictions/$', main.views.user_profile.updated_food_restrictions, name='updated-food-restrictions'),
    url(r'^profile/me/picture/$', main.views.user_profile.get_profile_picture_form, name='profile-pic-form'),
    url(r'^profile/me/picture/submit/$', main.views.user_profile.submit_profile_picture_form, name='profile-pic-form-submit'),

    url(r'^admin/', include(admin.site.urls)),
]
