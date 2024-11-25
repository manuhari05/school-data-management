# these are rest_framework imports
from rest_framework import serializers

from .models import Departments

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = '__all__'