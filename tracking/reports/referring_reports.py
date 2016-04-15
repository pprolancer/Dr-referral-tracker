from django.db.models import Sum
from datetime import date, timedelta
from . import TemplateFileReport, register_report

REPORT_TYPE = 'referring_entity'
TEMPLATE_DIR = 'tracking/reports/referring_entity'


class ReferringReport(TemplateFileReport):
    ''' Base class for Email Reports'''

    def __init__(self, referring_entity=None, logger=None):
        self.referring_entity = referring_entity
        super(ReferringReport, self).__init__(logger=logger)

    def __str__(self):
        return '<{0}(setting={1}>)'.format(self.name, self.referring_entity)


@register_report(REPORT_TYPE, name='thankyou')
class ThankyouReport(ReferringReport):
    subject_tpl = 'Patient refferal status'
    template_file = '{}/thankyou.html'.format(TEMPLATE_DIR)

    def get_extra_context(self):
        from tracking.models import PatientVisit

        assert self.referring_entity, 'referring_entity should be set!'

        today = date.today()
        last_month = today.replace(day=1) - timedelta(days=1)
        last_12_month = (last_month - timedelta(days=364)).replace(day=1)

        last_month_count = PatientVisit.objects.filter(
            referring_entity=self.referring_entity,
            visit_date__range=(last_month.replace(day=1), last_month)).\
            aggregate(Sum('visit_count')).get('visit_count__sum') or 0
        if not last_month_count:
            self.logger.info('Skipping this because no visit record in '
                             'last month')
            self.skip()
            return

        last_12_month_count = PatientVisit.objects.filter(
            referring_entity=self.referring_entity,
            visit_date__range=(last_12_month, last_month)).\
            aggregate(Sum('visit_count')).get('visit_count__sum') or 0

        extra = {
            'name': self.referring_entity.entity_name,
            'last_month': last_month.strftime('%B %Y'),
            'last_month_count': last_month_count,
            'last_12_month': last_12_month.strftime('%B %Y'),
            'last_12_month_count': last_12_month_count,
        }
        return extra
