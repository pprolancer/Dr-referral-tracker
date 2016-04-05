from rest_framework import viewsets
from tracking.models import Organization
from .serializers import OrganizationSerializer


class OrganizationView(viewsets.ModelViewSet):
    '''
    rest view set for Organization resource
    '''

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
