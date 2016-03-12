from tracking.models import Organization, ReferringEntity
import autocomplete_light

autocomplete_light.register(Organization, search_fields=['org_name'], attrs={
        'data-autcomplete-minimum-characters': 3,
        'placeholder': 'Select Group',
        'style':'width:173px;'
    })
autocomplete_light.register(ReferringEntity, search_fields=['entity_name'], attrs={
        'data-autcomplete-minimum-characters': 3,
        'placeholder': 'Select Practitioner',
        'style':'width:173px;'
    })
