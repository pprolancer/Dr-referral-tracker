import sys
import pkgutil
import logging
import importlib
from django.template import Template, Context
from django.template.loader import render_to_string


class InvalidReportException(Exception):
    pass


class ReportManager(object):
    _report_registry = {}

    @classmethod
    def get_report_cls(cls, report_type, name):
        klass = (cls._report_registry.get(report_type) or {}
                 ).get(name)
        if klass is None:
            raise InvalidReportException(
                'Invalid ReferringReport with name "{}"'.format(name))
        return klass

    @classmethod
    def get_registered_reports(cls, report_type):
        return (cls._report_registry.get(report_type) or {}).keys()

    @classmethod
    def register_report(cls, report_type, report_name, klass):
        report_type_registry = ReportManager._report_registry.setdefault(
            report_type, {})
        if report_name in report_type_registry:
            raise AssertionError('Report with type={} and name={} already '
                                 'exists'.format(report_type, report_name))
        report_type_registry[report_name] = klass
        klass.name = report_name
        return klass


def register_report(report_type, name=None):
    '''
    a decorator to register a report with a name to system
    '''
    def decorator(cls):
        assert issubclass(cls, Report), \
            'cls should be subclass of ReferringReport'
        report_name = name or cls.__name__
        return ReportManager.register_report(report_type, report_name, cls)

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

    def get_extra_context(self):
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


def import_submodules(package_name):
    """ Import all submodules of a module, recursively

    :param package_name: Package name
    :type package_name: str
    :rtype: dict[types.ModuleType]
    """
    package = sys.modules[package_name]
    return {
        name: importlib.import_module(package_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }

__all__ = [TemplateFileReport, Report, ReportManager, register_report]
__all__.extend(import_submodules(__name__).keys())
