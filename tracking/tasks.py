from __future__ import absolute_import

from django.core.mail import send_mail
from celery.decorators import periodic_task
from celery.schedules import crontab
from Practice_Referral import settings
from tracking.models import ReferringReportSetting
from tracking.reports.referring_reports import ReportManager, \
    InvalidReportException
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def send_referring_reports(referring_report_settings):
    '''
    handle sending of referring report by given report settings objects
    '''
    logger.info('**** Handling %s report_settings...',
                len(referring_report_settings))
    for report_setting in referring_report_settings:
        referring_entity = report_setting.referring_entity
        email = referring_entity.entity_email
        if not email:
            logger.warn('No entity_email for [%s]!', referring_entity)
            continue
        try:
            ReportClass = ReportManager.get_report_cls(
                report_setting.report_name)
        except InvalidReportException:
            logger.warn('Unknown report [%s]!', report_setting.report_name)
            continue

        report = ReportClass(referring_entity=report_setting.referring_entity,
                             logger=logger)
        if report.skipped():
            logger.info('Report %s skipped!', report)
            continue

        subject = report.get_subject()
        body = report.get_body()
        logger.info('Sending Email from %s to %s: subject: %s, body: %s',
                    settings.DEFAULT_EMAIL_FROM, email, subject, body)
        send_mail(subject, body, settings.DEFAULT_EMAIL_FROM, [email],
                  fail_silently=True, html_message=body)


# @periodic_task(run_every=crontab(minute='*/1'))
@periodic_task(run_every=crontab(minute=0, hour=0))
def daily_reports_handler():
    '''
    daily reports handler
    python manage.py celeryd -B -l info
    '''
    send_referring_reports(ReferringReportSetting.objects.filter(
        period=ReferringReportSetting.PERIOD_DAILY).all())


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_week=1))
def weekly_reports_handler():
    '''
    weekly reports handler
    python manage.py celeryd -B -l info
    '''

    send_referring_reports(ReferringReportSetting.objects.filter(
        period=ReferringReportSetting.PERIOD_WEEKLY).all())


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_month=1))
def monthly_reports_handler():
    '''
    monthly reports handler
    python manage.py celeryd -B -l info
    '''

    send_referring_reports(ReferringReportSetting.objects.filter(
        period=ReferringReportSetting.PERIOD_MONTHLY).all())


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_month=1,
                                 month_of_year='*/3'))
def quarterly_reports_handler():
    '''
    quarterly reports handler
    python manage.py celeryd -B -l info
    '''

    send_referring_reports(ReferringReportSetting.objects.filter(
        period=ReferringReportSetting.PERIOD_QUARTERLY).all())


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_month=1,
               month_of_year=1))
def yealy_reports_handler():
    '''
    yearly reports handler
    python manage.py celeryd -B -l info
    '''

    send_referring_reports(ReferringReportSetting.objects.filter(
        period=ReferringReportSetting.PERIOD_YEARLY).all())
