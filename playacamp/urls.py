from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views

import main.views.index
import main.views.user_profile

admin.autodiscover()

# Examples:
# url(r'^$', 'playacamp.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [     # pylint: disable=invalid-name
    url(r'^$', main.views.index.get, name='index'),
    url(r'^login/$', auth_views.LoginView.as_view()),
    url(r'^profile/(?P<user_id>\d+)$', main.views.user_profile.get),
    url(r'^profile/me/$', main.views.user_profile.get),
    url(r'^profile/me/attendance/$', main.views.user_profile.change_attending, name='change-attending'),
    url(r'^admin/', include(admin.site.urls)),
]
