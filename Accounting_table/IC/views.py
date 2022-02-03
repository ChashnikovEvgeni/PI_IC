from django.http import HttpResponse, Http404
from django.shortcuts import render  # шаблонизатор фреймворка Django
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import *
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import *


def index(request):
    # return HttpResponse("Страница приложения")
    return render(request, 'IC/index.html')


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()

    if len(queryset) == 0:
        raise Http404()

    serializer_class = ServiceSerializer

    # def stronge (self, request, *args, **kwargs):
    #   return render(request, 'IC/index.html')


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()

    if len(queryset) == 0:
        raise Http404()

    serializer_class = DepartmentSerializer

    @action(detail=False, methods=['get', 'post', 'put', 'delete'], name='report_departments')
    def report_departments(self, request, *args, **kwargs):
        return render(request, 'IC/report_departments.html', {'list': self.queryset})

    # lookup_field = 'Indicator'


# def get_object(self):
#  obj = Department.objects.get(Indicator = self.kwargs('Indicator'))
#   return obj


class IndicatorViewSet(ModelViewSet):
    queryset = Indicator.objects.select_related('department')

    if len(queryset) == 0:
        raise Http404()

    serializer_class = IndicatorSerializer

    @action(detail=False, methods=['get', 'post', 'put', 'delete'], name='Settlement form')
    def settlement_form(self, request, *args, **kwargs):
        print(self.queryset)
        return render(request, 'IC/settlement_form.html', {'list': self.queryset})

    @action(detail=False, methods=['get', 'post', 'put', 'delete'], name='Data input')
    def data_input(self, request, *args, **kwargs):
        print(self.queryset)
        return render(request, 'IC/data_input.html', {'list': self.queryset})


# lookup_field = 'department'
# def get_object(self):
#   obj = Indicator.object.get()
#  return obj


class Critical_serviceViewSet(ModelViewSet):
    queryset = Critical_service.objects.all()

    if len(queryset) == 0:
        raise Http404()

    serializer_class = Critical_serviceSerializer


# permission_classes = [IsOwnerOrStaffOrReadOnly]
# как пользоваться фильтрами, поиском, сортировкой
# filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
# filter_fields = ['target_indicator']
# если ищем по более чем одному полю, тогда search
# search_fields = ['target_indicator','actual_indicator']
# адрес по следующему формату
# http://127.0.0.1:8000/IC/Indicator/?search=90.0
# сортировка
# rdering_fields = ['department']

# def perform_create(self, serializer):
#     serializer.validated_data['owner'] = self.request.user
#    serializer.save()


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
