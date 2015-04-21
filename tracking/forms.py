from django import forms
from tracking.models import *
from phonenumber_field.formfields import PhoneNumberField

class OrganizationForm(forms.ModelForm):
    """
    Create a new organization,
    Check for duplicates
    Offer new NewPhysician creation in same form.
    """

    class Meta:
        model = Organization
        fields = ["org_name", "org_contact_name", "org_phone",
         "org_email", "org_special"]

class PhysicianForm(forms.ModelForm):
    """
    Create a new Physician
    autocomplete Organization https://github.com/yourlabs/django-autocomplete-light/tree/stable/2.x.x
    Check for duplicates
    Offer new NewPhysician creation
    """

    class Meta:
        model = Physician
        fields = ["physician_name", "physician_phone", "physician_email",
         "referral_special"]

class ReferralForm(forms.ModelForm):
    """
    record a new referral
    autocomplete Physician
    Don't need blank for Org
    Assume today's date
    """

    class Meta:
        model = Referral
        fields = ["visit_date", "visit_count"]

