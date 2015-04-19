from django import forms

class NewOrg(forms.Form):
    """
    Create a new organization,
    Check for duplicates
    Offer new NewPhysician creation in same form.
    """

class NewPhysician(forms.Form):
    """
    Create a new Physician
    autocomplete Organization https://github.com/yourlabs/django-autocomplete-light/tree/stable/2.x.x
    Check for duplicates
    Offer new NewPhysician creation
    """

class NewReferral(forms.Form):
    """
    record a new referral
    autocomplete Physician
    Don't need blank for Org
    Assume today's date
    """
