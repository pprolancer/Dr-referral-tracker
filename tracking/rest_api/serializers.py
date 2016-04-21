import inspect
import sys
from tracking.models import Organization, ReferringReportSetting, \
    ClinicUserReportSetting, TrackedModel, ClinicBaseModel
from rest_framework import serializers


class OrganizationSerializer(serializers.ModelSerializer):
    '''
    a serializer for Organization resource
    '''
    class Meta:
        model = Organization


class ReferringReportSettingSerializer(serializers.ModelSerializer):
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


class ClinicUserReportSettingSerializer(serializers.ModelSerializer):
    '''
    a serializer for ClinicUserReportSetting resource
    '''
    class Meta:
        model = ClinicUserReportSetting


class BulkClinicUserReportSettingSerializer(serializers.ModelSerializer):
    '''
    a serializer for bulk ClinicUserReportSetting resource
    '''
    class Meta:
        model = ClinicUserReportSetting
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
        if issubclass(model, ClinicBaseModel):
            exclude = tuple(getattr(klass.Meta, 'exclude', None) or ())
            klass.Meta.exclude = exclude + ('clinic',)
