from django.conf.urls import patterns, url

urlpatterns = patterns('googlesheets.views',
    url(r'^$', 'index'),
    url(r'^(?P<ship_id>\d+)/$', 'detail'),
    url(r'^(?P<ship_id>\d+)/results/$', 'results'),
    url(r'^entershipment/$', 'entershipment'),
	#url(r'^oauth2callback', 'auth_return'),
)

