import logging
from django.db.models import Sum
from datetime import date, timedelta
from django.template import Template, Context
from django.template.loader import render_to_string


class InvalidReportException(Exception):
    pass


class ReportManager(object):
    _report_registry = {}

    @staticmethod
    def get_report_cls(name):
        klass = ReportManager._report_registry.get(name)
        if klass is None:
            raise InvalidReportException(
                'Invalid ReferringReport with name "%s"' % name)
        return klass

    @staticmethod
    def get_registered_reports():
        return ReportManager._report_registry.keys()


def register_report(name=None):
    '''
    a decorator to register a report with a name to system
    '''
    def decorator(cls):
        assert issubclass(cls, ReferringReport), \
            'cls should be subclass of ReferringReport'
        report_name = name or cls.__name__
        if report_name in ReportManager._report_registry:
            raise AssertionError('ReferringReport with name=%s '
                                 'already exists' % report_name)
        cls.name = report_name
        ReportManager._report_registry[report_name] = cls
        return cls
    return decorator


class ReferringReport(object):
    ''' Base class for Email Reports'''

    name = None
    subject_tpl = 'Report: {{REPORT_NAME}}'
    body_tpl = ''
    _skip = False  # you can skip this email report by setting this flag

    @staticmethod
    def render_string_template(s, ctx):
        t = Template(s)
        c = Context(ctx or {})
        return t.render(c)

    def __init__(self, referring_entity=None, logger=None):
        self.logger = logger or logging
        self.referring_entity = referring_entity
        self.context = dict(referring_entity=referring_entity,
                            REPORT_NAME=self.name)
        self.context.update(self.get_extra_context() or {})

    def skip(self, status=True):
        ''' set this report as a skipped '''

        self._skip = status

    def skipped(self):
        return self._skip

    def get_extra_context():
        '''
        get extra context to be inject in body.
        this can be implemented in child classes
        '''

        return {}

    def get_subject(self):
        '''
        get subject of report
        this can be implemented in child classes
        '''

        return self.render_string_template(self.subject_tpl, self.context)

    def get_body(self):
        '''
        get subject of report
        this can be implemented in child classes
        '''

        return self.render_string_template(self.body_tpl, self.context)

    def __str__(self):
        return '<{0}(setting={1}>'.format(self.name, self.referring_entity)


class TemplateFileReferringReport(ReferringReport):
    ''' Base class for Email Report to use a template file to generate body '''

    template_file = None

    def __init__(self, *args, **kwargs):
        assert self.template_file is not None, 'should specify template_file'
        super(TemplateFileReferringReport, self).__init__(*args, **kwargs)

    def get_body(self):
        return render_to_string(self.template_file, self.context)


@register_report(name='thankyou')
class ThankyouReport(TemplateFileReferringReport):
    subject_tpl = 'Patient refferal status'
    template_file = 'tracking/reports/thankyou.html'

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
