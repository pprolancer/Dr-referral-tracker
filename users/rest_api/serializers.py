from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    '''
    a serializer for User resource
    '''
    class Meta:
        model = User
        exclude = ('password',)


class SessionSerializer(serializers.Serializer):
    '''
    a serializer for User resource
    '''
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)
