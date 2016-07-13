from datetime import datetime, timedelta
from django.db.models import Sum
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


class ClinicViewSetMixin(object):
    '''
    a base modelviewset class for all other viewsets
    '''
    def clinic_filter(self, qs):
        return qs.filter(clinic=self.request.clinic)

    def get_queryset(self):
        return self.clinic_filter(
            super(ClinicViewSetMixin, self).get_queryset())


class OrganizationView(PaginationPageSizeMixin, ClinicViewSetMixin,
                       viewsets.ModelViewSet):
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


class ReferringEntityView(PaginationPageSizeMixin, ClinicViewSetMixin,
                          viewsets.ModelViewSet):
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


class TreatingProviderView(PaginationPageSizeMixin, ClinicViewSetMixin,
                           viewsets.ModelViewSet):
    '''
    rest view for TreatingProvider resource
    '''
    max_page_size = 0  # zero mean unlimitted page_size
    queryset = TreatingProvider.objects.all()
    serializer_class = TreatingProviderSerializer
    filter_fields = ('provider_name', 'provider_title', 'provider_type')
    ordering_fields = '__all__'
    ordering = ('id',)


class PatientVisitView(ClinicViewSetMixin, viewsets.ModelViewSet):
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


class PatientVisitReportView(ClinicViewSetMixin, viewsets.GenericViewSet):
    '''
    rest view for PatientVisitReport
    '''

    queryset = PatientVisit.objects.all()

    def __count_struct(self):
        return {'mtd': 0, 'mtd_last': 0, 'ytd': 0, 'ytd_last': 0,
                'today': 0, 'yesterday': 0}

    def list(self, request, *args, **kwargs):
        orgs = self.clinic_filter(Organization.objects)
        org_entities = {}
        for r in self.clinic_filter(ReferringEntity.objects):
            entity = {'id': r.id, 'entity_name': r.entity_name,
                      'counts': self.__count_struct()}
            org_entities.setdefault(r.organization_id, {})[r.id] = entity

        data = {}
        for o in orgs:
            data[o.id] = {
                'id': o.id, 'org_name': o.org_name,
                'counts': self.__count_struct(),
                'entities': org_entities.get(o.id, {})}

        qs = self.get_queryset().values(
            'referring_entity', 'referring_entity__organization'
        ).annotate(visit_counts=Sum('visit_count'))

        today = datetime.today()
        yesterday = today - timedelta(days=1)
        last_year = today.year - 1
        date_ranges = {
            'mtd': (today.replace(day=1), today),
            'mtd_last': (today.replace(day=1, year=last_year),
                         today.replace(year=last_year)),
            'ytd': (today.replace(day=1, month=1), today),
            'ytd_last': (today.replace(day=1, month=1, year=last_year),
                         today.replace(year=last_year)),
            'today': (today, today),
            'yesterday': (yesterday, yesterday)
        }
        for k, date_range in date_ranges.items():
            for r in qs.filter(visit_date__range=date_range):
                org_id = r['referring_entity__organization']
                entity_id = r['referring_entity']
                count = r['visit_counts']
                org_data = data[org_id]
                org_data['counts'][k] += count
                org_data['entities'][entity_id]['counts'][k] = count

        return Response(data)


class ReferringReportSettingView(ClinicViewSetMixin, viewsets.ModelViewSet):
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

        ref_query = self.clinic_filter(ReferringEntity.objects)
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


class ClinicReportSettingView(ClinicViewSetMixin, viewsets.ModelViewSet):
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

        cu_query = self.clinic_filter(ClinicUser.objects)
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
