import inspect
import sys
from tracking.models import Organization, ReferringReportSetting, \
    ClinicUserReportSetting, TrackedModel
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
# dont touch this section we need this to set datetime fields of
# TrackedModel serializers as a readonly
# #############################################################################
def _perd(c):
    return inspect.isclass(c) and c.__module__ == _perd.__module__

classes = inspect.getmembers(sys.modules[__name__], _perd)
read_only_fields = ('creation_time', 'modification_time')
for class_name, klass in classes:
    if issubclass(klass, serializers.Serializer):
        meta = getattr(klass, 'Meta', None)
        if not meta:
            continue
        model = getattr(klass.Meta, 'model', None)
        if not model or not issubclass(model, TrackedModel):
            continue
        klass.Meta.read_only_fields = (getattr(klass.Meta, 'read_only_fields',
                                               None) or ()) + read_only_fields
