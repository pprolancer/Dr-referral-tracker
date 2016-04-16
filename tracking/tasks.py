from __future__ import absolute_import

from django.core.mail import send_mail
from celery.decorators import periodic_task
from celery.schedules import crontab
from Practice_Referral import settings
from tracking.models import ReferringReportSetting, ClinicUserReportSetting
from tracking.reports import ReportManager, InvalidReportException
from tracking.reports.referring_reports import REPORT_TYPE \
    as REFERRING_REPORT_TYPE
from tracking.reports.clinic_user_reports import REPORT_TYPE \
    as CLINIC_USER_REPORT_TYPE
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def _send_report(report, email):
    ''' send a report to an email '''
    if report.skipped():
        logger.info('Report %s skipped!', report)
        return

    subject = report.get_subject()
    body = report.get_body()
    logger.info('Sending Email from %s to %s: subject: %s, body: %s',
                settings.DEFAULT_EMAIL_FROM, email, subject, body)
    send_mail(subject, body, settings.DEFAULT_EMAIL_FROM, [email],
              fail_silently=True, html_message=body)


def send_referring_reports(referring_report_settings):
    '''
    handle sending of referring report by given report settings objects
    '''
    logger.info('**** Handling %s referring_report_settings...',
                len(referring_report_settings))
    for report_setting in referring_report_settings:
        referring_entity = report_setting.referring_entity
        email = referring_entity.entity_email
        if not email:
            logger.warn('No entity_email for [%s]!', referring_entity)
            continue
        try:
            ReportClass = ReportManager.get_report_cls(
                REFERRING_REPORT_TYPE, name=report_setting.report_name)
        except InvalidReportException:
            logger.warn('Unknown report [%s]!', report_setting.report_name)
            continue

        report = ReportClass(referring_entity=report_setting.referring_entity,
                             logger=logger)
        _send_report(report, email)


def send_clinic_user_reports(clinic_user_report_settings):
    '''
    handle sending of referring report by given report settings objects
    '''
    logger.info('**** Handling %s clinic_user_report_settings...',
                len(clinic_user_report_settings))
    for report_setting in clinic_user_report_settings:
        clinic_user = report_setting.clinic_user
        email = clinic_user.user.email
        if not email:
            logger.warn('No entity_email for [%s]!', clinic_user)
            continue
        try:
            ReportClass = ReportManager.get_report_cls(
                CLINIC_USER_REPORT_TYPE, name=report_setting.report_name)
        except InvalidReportException:
            logger.warn('Unknown report [%s]!', report_setting.report_name)
            continue

        report = ReportClass(clinic_user=report_setting.clinic_user,
                             logger=logger)
        _send_report(report, email)


def _get_referring_report_setting(period):
    return ReferringReportSetting.objects.filter(
        period=period, enabled=True).all()


def _get_clinic_user_report_setting(period):
    return ClinicUserReportSetting.objects.filter(
        period=period, enabled=True).all()


# @periodic_task(run_every=crontab(minute='*/1'))
@periodic_task(run_every=crontab(minute=0, hour=0))
def daily_reports_handler():
    '''
    daily reports handler
    python manage.py celeryd -B -l info
    '''
    try:
        send_referring_reports(_get_referring_report_setting(
            period=ReferringReportSetting.PERIOD_DAILY))
    except Exception as e:
        logger.exception(e)

    try:
        send_clinic_user_reports(_get_clinic_user_report_setting(
            period=ClinicUserReportSetting.PERIOD_DAILY))
    except Exception as e:
        logger.exception(e)


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_week=1))
def weekly_reports_handler():
    '''
    weekly reports handler
    python manage.py celeryd -B -l info
    '''

    try:
        send_referring_reports(_get_referring_report_setting(
            period=ReferringReportSetting.PERIOD_WEEKLY))
    except Exception as e:
        logger.exception(e)

    try:
        send_clinic_user_reports(_get_clinic_user_report_setting(
            period=ClinicUserReportSetting.PERIOD_WEEKLY))
    except Exception as e:
        logger.exception(e)


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_month=1))
def monthly_reports_handler():
    '''
    monthly reports handler
    python manage.py celeryd -B -l info
    '''

    try:
        send_referring_reports(_get_referring_report_setting(
            period=ReferringReportSetting.PERIOD_MONTHLY))
    except Exception as e:
        logger.exception(e)

    try:
        send_clinic_user_reports(_get_clinic_user_report_setting(
            period=ClinicUserReportSetting.PERIOD_MONTHLY))
    except Exception as e:
        logger.exception(e)


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_month=1,
                                 month_of_year='*/3'))
def quarterly_reports_handler():
    '''
    quarterly reports handler
    python manage.py celeryd -B -l info
    '''

    try:
        send_referring_reports(_get_referring_report_setting(
            period=ReferringReportSetting.PERIOD_QUARTERLY))
    except Exception as e:
        logger.exception(e)

    try:
        send_clinic_user_reports(_get_clinic_user_report_setting(
            period=ClinicUserReportSetting.PERIOD_QUARTERLY))
    except Exception as e:
        logger.exception(e)


@periodic_task(run_every=crontab(hour=0, minute=0, day_of_month=1,
               month_of_year=1))
def yealy_reports_handler():
    '''
    yearly reports handler
    python manage.py celeryd -B -l info
    '''

    try:
        send_referring_reports(_get_referring_report_setting(
            period=ReferringReportSetting.PERIOD_YEARLY))
    except Exception as e:
        logger.exception(e)

    try:
        send_clinic_user_reports(_get_clinic_user_report_setting(
            period=ClinicUserReportSetting.PERIOD_YEARLY))
    except Exception as e:
        logger.exception(e)
