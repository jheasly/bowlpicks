from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from bowlpicks.core.views import HomePage


urlpatterns = patterns('',
    url(r'^$', HomePage.as_view(), {}, 'homepage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
)
