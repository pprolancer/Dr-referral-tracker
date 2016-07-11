import inspect
import sys
from tracking.models import Organization, ReferringReportSetting, \
    ClinicReportSetting, TrackedModel, ClinicBaseModel, ReferringEntity, \
    TreatingProvider, PatientVisit
from rest_framework import serializers
from Practice_Referral import DynamicFieldsSerializerMixin


class OrganizationSerializer(DynamicFieldsSerializerMixin,
                             serializers.ModelSerializer):
    '''
    a serializer for Organization resource
    '''
    class Meta:
        model = Organization


class RelOrganizationSerializer(serializers.ModelSerializer):
    '''
    a serializer for Organization resource
    '''
    class Meta:
        model = Organization
        fields = ('id', 'org_name')


class ReferringEntitySerializer(DynamicFieldsSerializerMixin,
                                serializers.ModelSerializer):
    '''
    a serializer for ReferringEntity resource
    '''
    _organization = RelOrganizationSerializer(read_only=True,
                                              source='organization')

    class Meta:
        model = ReferringEntity


class RelReferringEntitySerializer(serializers.ModelSerializer):
    '''
    a serializer for ReferringEntity resource
    '''
    class Meta:
        model = ReferringEntity
        fields = ('id', 'entity_name')


class TreatingProviderSerializer(DynamicFieldsSerializerMixin,
                                 serializers.ModelSerializer):
    '''
    a serializer for TreatingProvider resource
    '''
    class Meta:
        model = TreatingProvider


class RelTreatingProviderSerializer(serializers.ModelSerializer):
    '''
    a serializer for TreatingProvider resource
    '''
    class Meta:
        model = TreatingProvider
        fields = ('id', 'provider_name')


class PatientVisitSerializer(DynamicFieldsSerializerMixin,
                             serializers.ModelSerializer):
    '''
    a serializer for PatientVisit resource
    '''
    _referring_entity = RelReferringEntitySerializer(read_only=True,
                                                     source='referring_entity')
    _treating_provider = RelTreatingProviderSerializer(
        read_only=True, source='treating_provider')

    class Meta:
        model = PatientVisit


class ReferringReportSettingSerializer(DynamicFieldsSerializerMixin,
                                       serializers.ModelSerializer):
    '''
    a serializer for ReferringReportSetting resource
    '''
    class Meta:
        model = ReferringReportSetting


class BulkReferringReportSettingSerializer(serializers.ModelSerializer):
    '''
    a serializer for bulk ReferringReportSetting resource
    '''
    class Meta:
        model = ReferringReportSetting
        exclude = ('id', 'referring_entity',)


class ClinicReportSettingSerializer(DynamicFieldsSerializerMixin,
                                    serializers.ModelSerializer):
    '''
    a serializer for ClinicReportSetting resource
    '''
    class Meta:
        model = ClinicReportSetting


class BulkClinicReportSettingSerializer(serializers.ModelSerializer):
    '''
    a serializer for bulk ClinicReportSetting resource
    '''
    class Meta:
        model = ClinicReportSetting
        exclude = ('id', 'clinic_user',)


# #############################################################################
# dont touch this section we need this section to hack some serializers
# to inject some data
# #############################################################################
def _perd(c):
    return inspect.isclass(c) and c.__module__ == _perd.__module__

classes = inspect.getmembers(sys.modules[__name__], _perd)
read_only_fields = ('creation_time', 'modification_time')
for class_name, klass in classes:
    if issubclass(klass, serializers.ModelSerializer):
        meta = getattr(klass, 'Meta', None)
        if not meta:
            continue
        model = getattr(klass.Meta, 'model', None)
        if not model:
            continue
        if issubclass(model, TrackedModel):
            rof = tuple(getattr(klass.Meta, 'read_only_fields', None) or ())
            klass.Meta.read_only_fields = rof + read_only_fields
        if issubclass(model, ClinicBaseModel) and \
                not hasattr(klass.Meta, 'fields'):
            exclude = tuple(getattr(klass.Meta, 'exclude', None) or ())
            klass.Meta.exclude = exclude + ('clinic',)
