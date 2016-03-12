from django.conf.urls import patterns, include, url
from tracking.views import *


urlpatterns = patterns(
    '',
    url(r'^logout/$',LogoutView.as_view(), name="logout"),
    url(r'^home/$', IndexView.as_view(), name="index"),
    url(r'^add/organization/$', OrganizationView.as_view(), name="add-organization"),
    url(r'^add/referring_entity/$', ReferringEntityView.as_view(), name="add-referring-entity"),
    url(r'^add/patient_visit/$', PatientVisitView.as_view(), name="add-patient-visit"),
    url(r'^add/get-patient_visit-view/$', GetPatientVisitReport.as_view(), name="get-patient_visit-view"),
    url(r'^patient-visit-history/$', GetPatientVisitHistory.as_view(), name="patient-visit-history"),
    url(r'^edit/referring_entity/([0-9]+)/$', edit_referring_entity, name="edit-referring-entity"),
    url(r'^edit/organization/([0-9]+)/$', edit_organization, name="edit-organization"),
    url(r'^view/organizations/$', OrganizationListView.as_view(), name="view-organizations"),
    url(r'^view/referring_entities/$', ReferringEntityListView.as_view(), name="view-referring-entities"),
    url('', include('social.apps.django_app.urls', namespace='social')),

)
