from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'app.views.index', name='index'),
	# url(r'^update/$', 'app.views.updateWeather', name='updateWeather'),

    url(r'^admin/', include(admin.site.urls)),
)
