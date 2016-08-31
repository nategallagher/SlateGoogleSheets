import os
from django.conf.urls import patterns, include, url
#from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^googlesheets/', include('googlesheets.urls')),
	url(r'^shipping/', include('shipping.urls')), 
 	url(r'^oauth2callback', 'googlesheets.views.auth_return'),
 	
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
						{'template_name': 'googlesheets/login.html'}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
						{'document_root': os.path.join(os.path.dirname(__file__), 'static')}),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)
