import types
from django.conf import settings

CURRENT_CLINIC_ATTR_NAME = getattr(settings, 'CURRENT_CLINIC_ATTR_NAME',
                                   '_current_clinic')

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()


def _do_set_current_clinic(clinic_fun):
    setattr(_thread_locals, CURRENT_CLINIC_ATTR_NAME,
            types.MethodType(clinic_fun, _thread_locals))


def _set_current_clinic(clinic=None):
    '''
    Sets current clinic in local thread.

    Can be used as a hook e.g. for shell jobs (when request object is not
    available).
    '''
    _do_set_current_clinic(lambda self: clinic)


class CurrentClinicMiddleware(object):
    def process_request(self, request):
        # fixme: this should be implemented in future according subdomain
        from tracking.models import Clinic
        request.clinic = Clinic.objects.order_by('id').first()

        _do_set_current_clinic(lambda self: getattr(request, 'clinic', None))


def get_current_clinic():
    current_clinic = getattr(_thread_locals, CURRENT_CLINIC_ATTR_NAME, None)
    return current_clinic() if current_clinic else current_clinic


def get_current_clinic_id():
    clinic = get_current_clinic()
    return clinic and clinic.id
