from django.db.models import Sum
from datetime import date, timedelta
from . import TemplateFileReport, register_report

REPORT_TYPE = 'clinic_user'
TEMPLATE_DIR = 'tracking/reports/clinic_user'


class ClinicUserReport(TemplateFileReport):
    ''' Base class for Email Reports'''

    def __init__(self, clinic_user=None, logger=None):
        self.clinic_user = clinic_user
        super(ClinicUserReport, self).__init__(logger=logger)

    def __str__(self):
        return '<{0}(setting={1}>'.format(self.name, self.clinic_user)


@register_report(REPORT_TYPE, name='visit_history')
class VisitHistoryReport(ClinicUserReport):
    subject_tpl = 'Patient visit history report'
    template_file = '{}/visit_history.html'.format(TEMPLATE_DIR)

    def get_extra_context(self):
        from tracking.models import PatientVisit

        assert self.clinic_user, 'clinic_user should be set!'
        today = date.today()
        visit_date = today - timedelta(days=1)

        clinic = self.clinic_user.clinic
        patient_visits = PatientVisit.objects.filter(
            treating_provider__clinic=clinic,
            visit_date=visit_date).order_by('-visit_date')

        extra = {
            'patient_visits': patient_visits,
            'name': self.clinic_user.user.username,
            'visit_date': visit_date.strftime('%B %d, %Y'),
        }
        return extra
