from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^cheques/', include('cheques.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
