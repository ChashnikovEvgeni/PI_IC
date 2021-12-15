from rest_framework.serializers import ModelSerializer

from IC.models import *


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class DepartmentSerializer(ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class IndicatorSerializer(ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'


