from django.conf.urls import patterns, include, url
from tracking.views import *


urlpatterns = patterns(
    '',
    url(r'^logout/$',LogoutView.as_view(), name="logout"),
    url(r'^home/$', IndexView.as_view(), name="index"),
    url(r'^add/organization/$', OrganizationView.as_view(), name="add-organization"),
    url(r'^add/physician/$', PhysicianView.as_view(), name="add-physician"),
    url(r'^add/referral/$', ReferralView.as_view(), name="add-referral"),
    url(r'^add/get-referral-view/$', GetReferralReport.as_view(), name="get-referral-view"),
    url(r'^referral-history/$', GetReferralHistory.as_view(), name="referral-history"),
    url(r'^edit/physician/([0-9])/$', edit_physician, name="edit-physician"),
    url(r'^edit/organization/([0-9])/$', edit_organization, name="edit-organization"),
    url('', include('social.apps.django_app.urls', namespace='social')),

)
