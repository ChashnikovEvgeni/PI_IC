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
        # fields = ('Department_name', 'title', 'units', 'comment', 'target_indicator', 'Significance_of_indicator', 'Plan', 'actual_indicator', 'Degree_of_compliance')
    # Determine the fields to apply...


class Critical_serviceSerializer(ModelSerializer):
    class Meta:
        model = Critical_service
        fields = '__all__'
