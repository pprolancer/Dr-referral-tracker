from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User, BaseUserManager

# Create your models here.


def custom_create_user(username, email=None, password=None, **extra_fields):
    """
    Creates and saves a User with the given username, email and password.
    """
    now = timezone.now()
    if not username:
        raise ValueError('The given username must be set')
    email = BaseUserManager.normalize_email(email)
    user_fields = dict(
        username=username, email=email, is_staff=False, is_active=True,
        is_superuser=False, date_joined=now,
    )
    user_fields.update(extra_fields)
    user = User(**user_fields)
    user.set_password(password)
    user.save()
    return user


def social_auth_custom_create_user(strategy, details, user=None, *args,
                                   **kwargs):
    if user:
        return {'is_new': False}

    USER_FIELDS = ['username', 'email']

    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    fields['is_active'] = False
    return {
        'is_new': True,
        'user': custom_create_user(**fields)
    }
