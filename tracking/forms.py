from django import forms
import autocomplete_light
from datetime import date
from tracking.models import *


class OrganizationForm(forms.ModelForm):
    """
    Create a new organization,
    Check for duplicates
    Offer new NewReferringEntity creation in same form.
    """

    required_css_class = 'required'

    class Meta:
        model = Organization
        exclude = ['creation_time','modification_time','clinic']
        
    def __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        self.fields['org_type'].required = True


class ReferringEntityForm(autocomplete_light.ModelForm):
    """
    Create a new ReferringEntity
    autocomplete Organization https://github.com/yourlabs/django-autocomplete-light/tree/stable/2.x.x
    Check for duplicates
    Offer new NewReferringEntity creation
    """

    required_css_class = 'required'

    class Meta:
        model = ReferringEntity
        exclude = ['creation_time','modification_time']


class PatientVisitForm(autocomplete_light.ModelForm):
    """
    record a new patient_visit
    autocomplete PatientVisit
    Don't need blank for Org
    Assume today's date
    """

    required_css_class = 'required'

    class Meta:
        model = PatientVisit
        exclude = ['creation_time','modification_time']

    def clean_visit_date(self):
        ''' check visit_date for greater than today '''
        visit_date = self.cleaned_data.get('visit_date')
        if visit_date and (visit_date > date.today()):
            raise forms.ValidationError(
                'visit_date cannot be greater than today')
        return visit_date


class TreatingProviderForm(autocomplete_light.ModelForm):
    """
    record a new treating_provider
    autocomplete TreatingProvider
    """

    required_css_class = 'required'

    class Meta:
        model = TreatingProvider
        exclude = ['creation_time','modification_time','clinic']        


class PatientVisitHistoryForm(forms.Form):
    """
    record a new patient_visit
    autocomplete ReferringEntity
    Don't need blank for Org
    Assume today's date
    """

    required_css_class = 'required'

    referring_entity = autocomplete_light.ModelMultipleChoiceField('ReferringEntityAutocomplete', required=False)
    from_date = forms.DateField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))
    to_date = forms.DateField(widget=forms.TextInput(attrs={'readonly' : 'readonly'}))


class GenericDeleteForm(forms.Form):
    '''
    generic form for delete entities. we use this to have csrf validation
    '''
    pass
