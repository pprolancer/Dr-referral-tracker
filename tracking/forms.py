from django import forms
from tracking.models import *

class OrganizationForm(forms.ModelForm):
    """
    Create a new organization,
    Check for duplicates
    Offer new NewPhysician creation in same form.
    """
    org_name = forms.CharField(label="Organization name", max_length=140)
    org_cont_name = forms.CharField(label="contact name", max_length=140)
    org_phone_no = forms.CharField(label="phone number", max_length=140)
    org_email = forms.CharField(label="email add", max_length=140)
    org_special = forms.BooleanField(label="special")

    class Meta:
        model = Organization


class PhysicianForm(forms.ModelForm):
    """
    Create a new Physician
    autocomplete Organization https://github.com/yourlabs/django-autocomplete-light/tree/stable/2.x.x
    Check for duplicates
    Offer new NewPhysician creation
    """
    physician_name = forms.CharField(label="Physician name", max_length=254)
    # physician_phone = forms.PhoneNumberField(label="Physician contact")
    physician_email = forms.EmailField(label="Physician email", max_length=254)
    referral_special = forms.BooleanField(label="Other referral type")

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
    visit_date = forms.DateField(label="Date of patient visit")
    visit_count = forms.IntegerField(label="Total Visits for day")

    class Meta:
        model = Referral
        fields = ["visit_date", "visit_count"]

