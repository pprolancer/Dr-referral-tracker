import autocomplete_light
from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Practice_Referral.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('tracking.urls')),
    url(r'^', include('social.apps.django_app.urls', namespace='social')),
    url(r'^', include('users.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
