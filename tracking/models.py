
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.forms.widgets import NumberInput

from phonenumber_field.modelfields import PhoneNumberField
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from datetime import datetime , timedelta, date
from django.db.models import Sum
from tracking.reports import ReportManager
from tracking.reports.referring_reports import REPORT_TYPE \
    as REFERRING_REPORT_TYPE
from tracking.reports.clinic_user_reports import REPORT_TYPE \
    as CLINIC_USER_REPORT_TYPE


today = date.today()
LAST_MONTH = date(day=1, month=today.month, year=today.year) - timedelta(days=1)
LAST_12_MONTH = LAST_MONTH - timedelta(days=364)

class TrackedModel(models.Model):
    creation_time = models.DateTimeField("Creation Timestamp", blank=True, null=True)
    modification_time = models.DateTimeField("Modification Timestamp", blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creation_time = timezone.now()
        self.modification_time = timezone.now()
        super(TrackedModel, self).save(*args, **kwargs)

class Clinic(TrackedModel):
    '''
    Top level entity, each entity will be linked to one,
    which might have one or more Users registered.
    Those Users are added through the admin interface.
    '''
    clinic_name = models.CharField(
        "Clinic Name", max_length=254, unique=True, blank=False, null=True)

    def __str__(self):
        return self.clinic_name

    @staticmethod
    def get_from_user(user):
        if not user.id:
            return None
        return ClinicUser.objects.filter(user=user).first().clinic

class ClinicUser(TrackedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey("Clinic")

    def __str__(self):
        return self.user.username

class Organization(TrackedModel):
    '''
    A ReferringEntity works for a Organization, (clinic, hospital, private practice...)
    Need a few "special Organizations"
        - Marketing
        - Patient
        - ? How can the user add special Organizations
        If org_special==True then only require org_name and call it PatientVisit group type
    https://github.com/stefanfoulis/django-phonenumber-field
    pip install django-phonenumber-field
    '''
    ORG_TYPE_MARKETING         = "MAR"
    ORG_TYPE_INSURANCE         = "INS"
    ORG_TYPE_INTERNAL          = "INT"
    ORG_TYPE_WORKCOMP          = "WKC"
    ORG_TYPE_HEATHCAREPROVIDER = "HCP"
    ORG_TYPE_CHOICES = (
        (ORG_TYPE_MARKETING        , "Marketing"          ),
        (ORG_TYPE_INSURANCE        , "Insurance"          ),
        (ORG_TYPE_INTERNAL         , "Internal"           ),
        (ORG_TYPE_WORKCOMP         , "Work comp."         ),
        (ORG_TYPE_HEATHCAREPROVIDER, "Healthcare Provider")
    )
    clinic = models.ForeignKey("Clinic")
    org_name = models.CharField(
        "Group Name", max_length=254, unique=True, blank=False, null=True)
    org_type = models.CharField(
        "Group Type", max_length=3, choices=ORG_TYPE_CHOICES, blank=True)
    org_contact_name = models.CharField(
        "Contact name", max_length=254, blank=True, null=True)
    org_phone = PhoneNumberField("Phone", blank=True)
    org_email = models.EmailField("Email address", max_length=254, blank=True)
    org_special = models.BooleanField("Special type", default=False)

    def get_absolute_url(self):
        return reverse('add-organization')

    def __str__(self):
        return self.org_name

    def get_referring_entity(self):
        referring_entitys_sort = self.ReferringEntity.filter().extra(
            select={'lower_entity_name': 'lower(entity_name)'}
            ).order_by('lower_entity_name')
        return referring_entitys_sort


class ReferringEntity(TrackedModel):
    """
    A ReferringEntity works for an Organization; clinic, hospital, private practice...
    Other patient_visit types for example; Other patient, google adds, website.....
    If entity_special==True then only require entity_name but call it "PatientVisit source"
    """
    organization = models.ForeignKey(
        Organization, related_name="ReferringEntity",verbose_name="Group")
    entity_name = models.CharField(
        "Name", max_length=254, unique=True, blank=False, null=True)
    entity_title = models.CharField("Title", max_length=50, blank=True)
    entity_phone = PhoneNumberField("Phone", blank=True)
    entity_email = models.EmailField(
        "Email address", max_length=254, blank=True)
    entity_special = models.BooleanField("Special type", default=False)

    def __str__(self):
        return self.entity_name

    def get_patient_visit(self, params, clinic):
        today = params['to_date']
        week_ago = params['from_date']
        patient_visit_sort = self.PatientVisit.filter(
            treating_provider__clinic=clinic,
            visit_date__range=(str(week_ago), str(today))).values('visit_date').annotate(visit=Sum('visit_count')).order_by('-visit_date')
        return patient_visit_sort

class TreatingProvider(TrackedModel):
    PROVIDER_TYPE_PHYSICIAN_ASSISTANT = "PA"
    PROVIDER_TYPE_DOCTOR              = "D"
    PROVIDER_TYPE_NURSE               = "N"
    PROVIDER_TYPE_NURSE_PRACTITIONER  = "NP"
    PROVIDER_TYPE_CHOICES = (
        (PROVIDER_TYPE_PHYSICIAN_ASSISTANT, "Physician Assistant"),
        (PROVIDER_TYPE_DOCTOR             , "Doctor"),
        (PROVIDER_TYPE_NURSE              , "Nurse"),
        (PROVIDER_TYPE_NURSE_PRACTITIONER , "Nurse Practitioner"),
    )
    clinic = models.ForeignKey("Clinic")
    provider_name = models.CharField(
        "Name", max_length=254, unique=True, blank=False, null=True)
    provider_title = models.CharField("Title", max_length=50, blank=True)
    provider_type = models.CharField(
        "Provider Type", max_length=2, choices=PROVIDER_TYPE_CHOICES, blank=True)

    def __str__(self):
        return self.provider_name


class PatientVisit(TrackedModel):
    """
    PatientVisit is a patient visit referred to the clinic from a "ReferringEntity" that is part of an "Organization"
    Not sure how to do the multiple ForeignKey or if that is right.
    """
    referring_entity = models.ForeignKey(
        ReferringEntity, related_name="PatientVisit",verbose_name="Referring Entity")
    treating_provider = models.ForeignKey(
        TreatingProvider, related_name="TreatingProvider",verbose_name="Treating Provider", null=True)
    visit_date = models.DateField("Visit Date", default=date.today)
    visit_appointment_time = models.TimeField("Appointment Time", blank=True, null=True, default=None)
    visit_actual_time = models.TimeField("Actual Time", blank=True, null=True, default=None)
    visit_count = models.PositiveIntegerField("Visit Count", default=1,
                                              validators=[MinValueValidator(1)])

    def __str__(self):
        return self.referring_entity.organization.org_name


class ReportSetting(TrackedModel):
    class Meta:
        abstract = True

    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'
    PERIOD_QUARTERLY = 'quarterly'
    PERIOD_YEARLY = 'yearly'

    PERIOD_CHOICES = (
        (PERIOD_DAILY, 'Daily'),
        (PERIOD_WEEKLY, 'Weekly'),
        (PERIOD_MONTHLY, 'Monthly'),
        (PERIOD_QUARTERLY, 'Quarterly'),
        (PERIOD_YEARLY, 'Yearly'),
    )
    enabled = models.BooleanField("Enabled", default=True)
    period = models.CharField("Report Period", max_length=16,
                              default=PERIOD_DAILY, choices=PERIOD_CHOICES,
                              blank=False, null=False)

    def __str__(self):
        return str(self.report_name)


class ReferringReportSetting(ReportSetting):
    REPORTS_CHOICES = tuple((r, r) for r in ReportManager.get_registered_reports(REFERRING_REPORT_TYPE))

    referring_entity = models.ForeignKey(ReferringEntity, blank=False,
                                         null=False, on_delete=models.CASCADE)
    report_name = models.CharField("Report Name", max_length=64,
                                   choices=REPORTS_CHOICES, blank=False,
                                   null=False)

    class Meta:
        unique_together = (("referring_entity", "report_name"),)


class ClinicUserReportSetting(ReportSetting):
    REPORTS_CHOICES = tuple((r, r) for r in ReportManager.get_registered_reports(CLINIC_USER_REPORT_TYPE))

    clinic_user = models.ForeignKey(ClinicUser, blank=False,
                                    null=False, on_delete=models.CASCADE)
    report_name = models.CharField("Report Name", max_length=64,
                                   choices=REPORTS_CHOICES, blank=False,
                                   null=False)

    class Meta:
        unique_together = (("clinic_user", "report_name"),)
