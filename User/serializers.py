# these are rest_framework imports
from rest_framework import serializers

from .models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only':True,'required': False},  # Make password optional
        }