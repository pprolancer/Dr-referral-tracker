import autocomplete_light
from rest_framework import routers
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tracking.rest_api.views import OrganizationView, \
    ReferringReportSettingView, ClinicUserReportSettingView
from users.rest_api.views import SessionView

# register all rest views here
rest_router = routers.DefaultRouter()
rest_router.register(r'session', SessionView, base_name='session')
rest_router.register(r'organization', OrganizationView)
rest_router.register(r'report_setting/referring', ReferringReportSettingView)
rest_router.register(r'report_setting/clinic_user',
                     ClinicUserReportSettingView)


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
    url(r'^api/v1/', include(rest_router.urls, namespace='rest_api')),
)
