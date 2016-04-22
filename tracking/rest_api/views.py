from rest_framework import viewsets
from rest_framework.response import Response
from tracking.models import Clinic, Organization, ReferringReportSetting, \
    ReferringEntity, ClinicUserReportSetting, ClinicUser
from .serializers import OrganizationSerializer, \
    ReferringReportSettingSerializer, BulkReferringReportSettingSerializer, \
    ClinicUserReportSettingSerializer, BulkClinicUserReportSettingSerializer


class OrganizationView(viewsets.ModelViewSet):
    '''
    rest view for Organization resource
    '''
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_fields = ('org_name', 'org_type', 'org_contact_name', 'org_phone',
                     'org_email', 'org_special')
    ordering_fields = '__all__'

    def get_queryset(self):
        return super(OrganizationView, self).get_queryset()\
            .filter(clinic=self.request.clinic)


class ReferringReportSettingView(viewsets.ModelViewSet):
    '''
    rest view for ReferringReportSetting resource
    '''

    queryset = ReferringReportSetting.objects.all()
    serializer_class = ReferringReportSettingSerializer
    filter_fields = ('period', 'report_name', 'enabled',
                     'referring_entity')
    ordering_fields = '__all__'

    def get_queryset(self):
        return super(ReferringReportSettingView, self).get_queryset()\
            .filter(referring_entity__organization__clinic=self.request.clinic)

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

        ref_query = ReferringEntity.objects.filter(
            organization__clinic=self.request.clinic)
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


class ClinicUserReportSettingView(viewsets.ModelViewSet):
    '''
    rest view for ClinicUserReportSetting resource
    '''

    queryset = ClinicUserReportSetting.objects.all()
    serializer_class = ClinicUserReportSettingSerializer
    filter_fields = ('period', 'report_name', 'enabled', 'clinic_user')
    ordering_fields = '__all__'

    def get_queryset(self):
        return super(ClinicUserReportSettingView, self).get_queryset()\
            .filter(clinic_user__clinic=self.request.clinic)

    def create(self, request, *args, **kwargs):
        bulk = (request.data or {}).pop('bulk', False)
        if bulk:
            return self.__bulk_create(request)
        return super(ClinicUserReportSettingView, self).create(request, *args,
                                                               **kwargs)

    def __bulk_create(self, request):
        serializer_class = BulkClinicUserReportSettingSerializer
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
            obj, created = ClinicUserReportSetting.objects.update_or_create(
                report_name=report_name, clinic_user=cu,
                defaults=serializer.data)
            ids.append(obj.id)
        return Response({'ids': ids})
