from rest_framework import viewsets
from rest_framework.response import Response

from Practice_Referral import PaginationPageSizeMixin
from tracking.models import Organization, ReferringReportSetting, \
    ReferringEntity, TreatingProvider, ClinicReportSetting, ClinicUser, \
    PatientVisit
from .serializers import OrganizationSerializer, \
    ReferringReportSettingSerializer, BulkReferringReportSettingSerializer, \
    ClinicReportSettingSerializer, BulkClinicReportSettingSerializer, \
    ReferringEntitySerializer, TreatingProviderSerializer, \
    PatientVisitSerializer


class BaseClinicModelViewSet(viewsets.ModelViewSet):
    '''
    a base modelviewset class for all other viewsets
    '''

    def get_queryset(self):
        return super(BaseClinicModelViewSet, self).get_queryset()\
            .filter(clinic=self.request.clinic)


class OrganizationView(PaginationPageSizeMixin, BaseClinicModelViewSet):
    '''
    rest view for Organization resource
    '''
    max_page_size = 0  # zero mean unlimitted page_size
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_fields = ('org_name', 'org_type', 'org_contact_name', 'org_phone',
                     'org_email', 'org_special')
    ordering_fields = '__all__'
    ordering = ('id',)


class ReferringEntityView(PaginationPageSizeMixin, BaseClinicModelViewSet):
    '''
    rest view for ReferringEntity resource
    '''
    max_page_size = 0  # zero mean unlimitted page_size
    queryset = ReferringEntity.objects.all()
    serializer_class = ReferringEntitySerializer
    filter_fields = ('organization', 'entity_name', 'entity_title',
                     'entity_phone', 'entity_email', 'entity_special')
    ordering_fields = '__all__'
    ordering = ('id',)


class TreatingProviderView(PaginationPageSizeMixin, BaseClinicModelViewSet):
    '''
    rest view for TreatingProvider resource
    '''
    max_page_size = 0  # zero mean unlimitted page_size
    queryset = TreatingProvider.objects.all()
    serializer_class = TreatingProviderSerializer
    filter_fields = ('provider_name', 'provider_title', 'provider_type')
    ordering_fields = '__all__'
    ordering = ('id',)


class PatientVisitView(BaseClinicModelViewSet):
    '''
    rest view for PatientVisit resource
    '''
    queryset = PatientVisit.objects.all()
    serializer_class = PatientVisitSerializer
    filter_fields = ('referring_entity', 'treating_provider', 'visit_date',
                     'visit_appointment_time', 'visit_actual_time',
                     'visit_count')
    ordering_fields = '__all__'
    ordering = ('id',)


class ReferringReportSettingView(BaseClinicModelViewSet):
    '''
    rest view for ReferringReportSetting resource
    '''

    queryset = ReferringReportSetting.objects.all()
    serializer_class = ReferringReportSettingSerializer
    filter_fields = ('period', 'report_name', 'enabled',
                     'referring_entity')
    ordering_fields = '__all__'

    def create(self, request, *args, **kwargs):
        bulk = (request.data or {}).pop('bulk', False)
        if bulk:
            return self.__bulk_create(request)
        return super(ReferringReportSettingView, self).create(request, *args,
                                                              **kwargs)

    def __bulk_create(self, request):
        serializer_class = BulkReferringReportSettingSerializer
        data = request.data
        referring_entities = data.pop('referring_entity', None)

        ref_query = ReferringEntity.objects.filter(clinic=self.request.clinic)
        if referring_entities == '*':
            pass
        elif isinstance(referring_entities, list):
            ref_query = ref_query.filter(id__in=tuple(referring_entities))
        else:
            return Response({'referring_entity': 'Invalid data'},
                            status=400)
        ids = []
        for ref in ref_query:
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            report_name = serializer.data['report_name']
            obj, created = ReferringReportSetting.objects.update_or_create(
                report_name=report_name, referring_entity=ref,
                defaults=serializer.data)
            ids.append(obj.id)
        return Response({'ids': ids})


class ClinicReportSettingView(BaseClinicModelViewSet):
    '''
    rest view for ClinicReportSetting resource
    '''

    queryset = ClinicReportSetting.objects.all()
    serializer_class = ClinicReportSettingSerializer
    filter_fields = ('period', 'report_name', 'enabled', 'clinic_user')
    ordering_fields = '__all__'

    def create(self, request, *args, **kwargs):
        bulk = (request.data or {}).pop('bulk', False)
        if bulk:
            return self.__bulk_create(request)
        return super(ClinicReportSettingView, self).create(request, *args,
                                                           **kwargs)

    def __bulk_create(self, request):
        serializer_class = BulkClinicReportSettingSerializer
        data = request.data
        clinic_users = data.pop('clinic_user', None)

        cu_query = ClinicUser.objects.filter(clinic=self.request.clinic)
        if clinic_users == '*':
            pass
        elif isinstance(clinic_users, list):
            cu_query = cu_query.filter(id__in=tuple(clinic_users))
        else:
            return Response({'clinic_user': 'Invalid data'},
                            status=400)
        ids = []
        for cu in cu_query:
            serializer = serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            report_name = serializer.data['report_name']
            obj, created = ClinicReportSetting.objects.update_or_create(
                report_name=report_name, clinic_user=cu,
                defaults=serializer.data)
            ids.append(obj.id)
        return Response({'ids': ids})
