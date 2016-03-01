from django.contrib import messages


def social_auth_check_activation(user, *args, **kwargs):
    request = kwargs['strategy'].request
    if not user:
        return
    if not user.is_active:
        msg = 'User is registered. but is not active yet! please be waiting '\
              'for admin to activate you.'
        messages.warning(request, msg)
