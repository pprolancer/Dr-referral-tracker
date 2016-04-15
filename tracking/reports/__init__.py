import os
import glob
import logging
from django.template import Template, Context
from django.template.loader import render_to_string


class InvalidReportException(Exception):
    pass


class ReportManager(object):
    _report_registry = {}

    @staticmethod
    def get_report_cls(report_type, name):
        klass = (ReportManager._report_registry.get(report_type) or {}
                 ).get(name)
        if klass is None:
            raise InvalidReportException(
                'Invalid ReferringReport with name "%s"' % name)
        return klass

    @staticmethod
    def get_registered_reports(report_type):
        return (ReportManager._report_registry.get(report_type) or {}).keys()


def register_report(report_type, name=None):
    '''
    a decorator to register a report with a name to system
    '''
    def decorator(cls):
        assert issubclass(cls, Report), \
            'cls should be subclass of ReferringReport'
        report_name = name or cls.__name__
        report_type_registry = ReportManager._report_registry.setdefault(
            report_type, {})
        if report_name in report_type_registry:
            raise AssertionError('Report with type=%s and name=%s '
                                 'already exists' % (report_type, report_name))
        cls.name = report_name
        report_type_registry[report_name] = cls
        return cls
    return decorator


class Report(object):
    ''' Base class for Reports'''

    name = None
    subject_tpl = 'Report: {{REPORT_NAME}}'
    body_tpl = ''
    _skip = False  # you can skip this email report by setting this flag

    @staticmethod
    def render_string_template(s, ctx):
        t = Template(s)
        c = Context(ctx or {})
        return t.render(c)

    def __init__(self, logger=None):
        self.logger = logger or logging
        self.context = dict(REPORT_NAME=self.name)
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
        return '<Report {0}>'.format(self.name)


class TemplateFileReport(Report):
    ''' Base class for Email Report to use a template file to generate body '''

    template_file = None

    def __init__(self, *args, **kwargs):
        assert self.template_file is not None, 'should specify template_file'
        super(TemplateFileReport, self).__init__(*args, **kwargs)

    def get_body(self):
        return render_to_string(self.template_file, self.context)


__all__ = [TemplateFileReport, Report, ReportManager, register_report]
files = glob.glob(os.path.dirname(__file__) + "/*.py")
for f in files:
    if os.path.isfile(f) and not os.path.basename(f).startswith('_'):
        mod = os.path.basename(f)[:-3]
        exec("from . import %s" % mod)
        __all__.append(mod)
