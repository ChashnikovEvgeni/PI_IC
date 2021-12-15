from django.http import HttpResponse
from django.shortcuts import render #шаблонизатор
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import *
from .serializers import *


def index(request):
    return HttpResponse("Страница приложения")


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer




class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class IndicatorViewSet(ModelViewSet):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer
    permission_classes = [IsAuthenticated]
    #как пользоваться фильтрами, поиском, сортировкой
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['target_indicator']
     # если ищем по более чем одному полю, тогда search
    search_fields = ['target_indicator','actual_indicator']
    # адрес по следующему формату
     # http://127.0.0.1:8000/IC/Indicator/?search=90.0
     #сортировка
    rdering_fields = ['department']


















def all_Indicators(request):
    Indicators = Indicator.objects.all()
    return HttpResponse({Indicators})


def all_Departments(request):
    Departments = Department.objects.all()
    return HttpResponse({Departments})


def all_Service(request):
    service = Service.objects.all()
    return HttpResponse({service})




def auth(request):
    return render(request, 'oauth.html')