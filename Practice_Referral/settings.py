"""
Django settings for Practice_Referral project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

try:
    from Practice_Referral.settings_production import *
except:
    from Practice_Referral.settings_development import *

# SECURITY WARNING: keep the secret key used in production secret!
# see settings_secret

# Application definition

INSTALLED_APPS = (
    'autocomplete_light',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'tracking',
    'social.apps.django_app.default',
    'djcelery',
    'Practice_Referral',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'Practice_Referral.urls'

WSGI_APPLICATION = 'Practice_Referral.wsgi.application'

# SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "collected_static")

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)


# celery specific settings

CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'

BROKER_URL = 'django://'

INSTALLED_APPS += ('kombu.transport.django', )

## Amazon ses settings

INSTALLED_APPS += ('django_ses', )


EMAIL_BACKEND = 'django_ses.SESBackend'
# EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_PORT = 465

EMAIL_USE_TLS = True

DEFAULT_EMAIL_FROM = "update@heteroskedastic.com"

# These are optional -- if they're set as environment variables they won't
# need to be set here as well

# Additionally, you can specify an optional region, like so:
# AWS_SES_REGION_NAME = 'us-east-1'
# AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'
