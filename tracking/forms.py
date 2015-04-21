from django import forms
from tracking.models import *


class OrganizationForm(forms.ModelForm):
    """
    Create a new organization,
    Check for duplicates
    Offer new NewPhysician creation in same form.
    """

    class Meta:
        model = Organization
        exclude = []


class PhysicianForm(forms.ModelForm):
    """
    Create a new Physician
    autocomplete Organization https://github.com/yourlabs/django-autocomplete-light/tree/stable/2.x.x
    Check for duplicates
    Offer new NewPhysician creation
    """

    class Meta:
        model = Physician
        exclude = []


class ReferralForm(forms.ModelForm):
    """
    record a new referral
    autocomplete Physician
    Don't need blank for Org
    Assume today's date
    """

    class Meta:
        model = Referral
        exclude = []
