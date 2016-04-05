from django.conf.urls import patterns, url
from users.views import *

urlpatterns = patterns(
    '',
    url(r'^user/register/$', RegisterView.as_view(), name="user_register"),
    url(r'^$', LoginView.as_view(), name="user_login"),
)
