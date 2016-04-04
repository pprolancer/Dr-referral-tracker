from django.conf.urls import patterns, url
from users.views import *
from users.rest_api.views import SessionView

urlpatterns = patterns(
    '',
    url(r'^user/register/$', RegisterView.as_view(), name="user_register"),
    url(r'^api/v1/session/$', SessionView.as_view()),
    url(r'^$', LoginView.as_view(), name="user_login"),
)
