from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, raise_errors_on_nested_writes
from IC.models import *


# Сериализатор не только работает с данными на считывание и выдачу, но и производит валидацию
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


class Indicators_fileSerializer(ModelSerializer):
    class Meta:
        model = Indicators_file
        fields = '__all__'


class Critical_serviceSerializer(ModelSerializer):
    class Meta:
        model = Critical_service
        fields = '__all__'
