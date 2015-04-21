from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from tracking.views import *


urlpatterns = patterns(
    '',
    url(r'^add/organization/$', Organization.as_view(), name="add-organization"),
    url(r'^add/physician/$', Physician.as_view(), name="add-physician"),
    url(r'^add/referral/$', Referral.as_view(), name="add-referral"),
)
