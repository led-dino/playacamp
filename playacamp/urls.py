from django.conf.urls import include, url
from django.contrib import admin

import main.views

admin.autodiscover()

# Examples:
# url(r'^$', 'playacamp.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [     # pylint: disable=invalid-name
    url(r'^$', main.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
]
