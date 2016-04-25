from django.db.models import Sum
from datetime import date, timedelta
from . import TemplateFileReport, register_report

REPORT_TYPE = 'clinic'
TEMPLATE_DIR = 'tracking/reports/clinic'


class ClinicReport(TemplateFileReport):
    ''' Base class for Email Reports'''

    def __init__(self, clinic=None, logger=None):
        self.clinic = clinic
        super(ClinicReport, self).__init__(logger=logger)

    def __str__(self):
        return '<{0}(setting={1}>'.format(self.name, self.clinic)


@register_report(REPORT_TYPE, name='visit_history')
class VisitHistoryReport(ClinicReport):
    subject_tpl = 'Patient visit history report'
    template_file = '{}/visit_history.html'.format(TEMPLATE_DIR)

    def get_extra_context(self):
        from tracking.models import PatientVisit

        assert self.clinic, 'clinic should be set!'
        today = date.today()
        visit_date = today - timedelta(days=1)

        patient_visits = PatientVisit.objects.filter(
            clinic=self.clinic,
            visit_date=visit_date).order_by('-visit_date')

        extra = {
            'patient_visits': patient_visits,
            'visit_date': visit_date.strftime('%B %d, %Y'),
        }
        return extra


@register_report(REPORT_TYPE, name='weekly_visit')
class WeeklyVisitReport(ClinicReport):
    subject_tpl = 'Weekly visit report ({{from_date}} - {{to_date}})'
    template_file = '{}/weekly_visit.html'.format(TEMPLATE_DIR)

    def get_extra_context(self):
        from tracking.models import PatientVisit, TreatingProvider

        assert self.clinic, 'clinic should be set!'
        today = date.today()
        start_week = today - timedelta(today.weekday())
        end_week = start_week + timedelta(4)
        start_month = today.replace(day=1)
        end_month = (today.replace(day=10) + timedelta(days=30)
                     ).replace(day=1) - timedelta(days=1)
        start_date = min(start_month, start_week)
        end_date = max(end_month, end_week)
        week_days = [start_week + timedelta(days=i) for i in range(5)]

        query = PatientVisit.objects.filter(
            referring_entity__organization__org_type__isnull=False,
            clinic=self.clinic, visit_date__range=(start_date, end_date)
            ).extra(select={
                'is_current': "tracking_organization.org_type='INT'"}
            ).values('visit_date', 'treating_provider__provider_name',
                     'is_current').annotate(total=Sum('visit_count')).all()
        data = {}
        has_no_name = False
        UNKNOWN_PVD = '<Unknown>'
        CLINIC_TOTAL = 'Clinic totals'
        MONTH_RANGE = 'Month'
        for r in query:
            provider = r['treating_provider__provider_name']
            visit_date = r['visit_date']
            if not provider:
                has_no_name = True
                provider = UNKNOWN_PVD
            val_idx = 0 if r['is_current'] else 1
            if visit_date >= start_week and visit_date <= end_week:
                vals = data.setdefault(visit_date,
                                       {}).setdefault(provider, [0, 0])
                vals[val_idx] += r['total']
            if visit_date >= start_month and visit_date <= end_month:
                vals = data.setdefault(MONTH_RANGE,
                                       {}).setdefault(provider, [0, 0])
                vals[val_idx] += r['total']

        providers = [t.provider_name for t in TreatingProvider.objects.filter(
            clinic=self.clinic).order_by('id').all()]
        if has_no_name:
            providers.append(UNKNOWN_PVD)

        records = []
        total_week = [[0, 0, 0] for i in range(len(week_days)+1)]
        for pvd in providers:
            row = [pvd]
            for i in range(len(week_days)+1):
                if i == len(week_days):
                    dt = MONTH_RANGE
                else:
                    dt = week_days[i]
                val = data.get(dt, {}).get(pvd, None) or [0, 0]
                val.append(val[0]+val[1])
                row.append(val)
                total_week[i][0] += val[0]
                total_week[i][1] += val[1]
                total_week[i][2] += val[2]
            records.append(row)

        records.insert(0, [CLINIC_TOTAL] + total_week)
        self.logger.info("records: %s", records)

        extra = {
            'from_date': start_week.strftime('%b %d, %Y'),
            'to_date': end_week.strftime('%b %d, %Y'),
            'week_days': week_days,
            'records': records,
        }
        return extra
