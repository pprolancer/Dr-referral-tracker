from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from tracking.views import *


urlpatterns = patterns('',

    # url(r'^welcome/$',TemplateView.as_view(template_name="registration/welcome.html"),name="welcome"),
    # url(r'^$', organization.as_view(), name="organization"),

    url(r'^$', organization.as_view(), name="organization"),
) 