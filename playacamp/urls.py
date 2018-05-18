from django.conf.urls import include, url
from django.contrib import admin

import main.views.index
import main.views.login
import main.views.user_profile
import main.views.signup

admin.autodiscover()

# Examples:
# url(r'^$', 'playacamp.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [     # pylint: disable=invalid-name
    url(r'^$', main.views.index.get, name='index'),
    url(r'^login/$', main.views.login.get, name='login'),
    url(r'^signup/$', main.views.signup.get, name='signup'),
    url(r'^signup/submit/$', main.views.signup.post, name='signup-submit'),
    url(r'^profiles/$', main.views.user_profile.list_profiles, name='user-profile-list'),
    url(r'^profile/(?P<user_id>\d+)$', main.views.user_profile.get, name='user-profile'),
    url(r'^profile/me/$', main.views.user_profile.get, name='user-profile-me'),
    url(r'^profile/me/attendance/$', main.views.user_profile.changed_attending, name='changed-attending'),
    url(r'^profile/me/skills/$', main.views.user_profile.updated_skills, name='updated-skills'),
    url(r'^profile/me/food-restrictions/$', main.views.user_profile.updated_food_restrictions, name='updated-food-restrictions'),
    url(r'^admin/', include(admin.site.urls)),
]
