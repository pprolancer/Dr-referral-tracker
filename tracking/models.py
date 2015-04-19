from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import EmailField


class Organization(models.Model):
    '''
    A Physician works for a Organization, (clinic, hospital, private practice...)
    Need a few "special Organizations"
        - Marketing
        - Patient
        - ? How can the user add special Organizations
        If org_special==True then only require org_name and call it Referral group type
    https://github.com/stefanfoulis/django-phonenumber-field
    '''
    org_name = models.CharField("Organization name", max_length=254, blank=False, null=True) #What does null mean?
    org_contact_name = models.CharField("Organization contact name", max_length=254, blank=False, null=True)
    org_phone = PhoneNumberField("Organization contact phone")
    org_email = EmailField("Organization contact email", max_length=254)
    org_special = BooleanField("Other group type")

class Physician(models.Model):
    """
    A Physician works for a Organization; clinic, hospital, private practice...
    Other referral types for example; Other patient, google adds, website.....
    If referral_special==True then only require physician_name but call it "Referral source"
    """
    organization = models.ForeignKey(Organization, related_name="Physician")
    physician_name = models.CharField("Physician name", max_length=254, blank=False, null=True)
    physician_phone = PhoneNumberField("Physician contact phone")
    physician_email = EmailField("Physician contact email", max_length=254)
    referral_special = BooleanField("Other referral type")
