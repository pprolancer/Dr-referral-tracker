from tracking.models import Organization
import autocomplete_light

autocomplete_light.register(Organization, search_fields=['org_name'])
