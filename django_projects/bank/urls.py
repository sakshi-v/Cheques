from django.contrib import admin
from django.conf.urls.defaults import *
admin.autodiscover()

urlpatterns = patterns('',
	(r'^api/', include('bank.api.urls')),
    (r'^cheques/', include('cheques.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
