from tracking.models import Organization
from rest_framework import serializers


class OrganizationSerializer(serializers.ModelSerializer):
    '''
    a serializer for Organization resource
    '''
    class Meta:
        model = Organization
