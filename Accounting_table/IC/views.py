from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404, HttpRequest
from django.shortcuts import render, redirect  # шаблонизатор фреймворка Django
from django.views.generic import CreateView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import renderers, permissions
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator

from .forms import *
from .models import *
from .permissions import IsOwnerOrStaffOrReadOnly
from .serializers import *
from .utils import *


def index(request):
    user_menu = menu
    return render(request, 'IC/index.html')


class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]


def forms_service(request, service_id=None):
    if service_id is None:
        service = None
        template = 'IC/add_object.html'
        context = {
            'url_name': 'add_service',
            'title': 'Добавление службы',
        }
    else:
        service = Service.objects.get(pk=service_id)
        template = 'IC/change_object.html'
        context = {
            'url_name': 'change_service',
            'title': 'Редактирование службы',
        }
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ServiceForm(instance=service)
        context['form'] = form
    return render(request, template, context)


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get', 'post', 'put', 'delete'], name='report_departments')
    def report_departments(self, request, *args, **kwargs):
        page_obj = get_page_obj(self.queryset, 1, request)
        return render(request, 'IC/report_departments.html',
                      {'page_obj': page_obj, 'list': self.queryset})


def forms_department(request, department_id=None):
    if department_id is None:
        department = None
        template = 'IC/add_object.html'
        context = {
            'url_name': 'add_department',
            'title': 'Добавление отдела/группы',
        }
    else:
        department = Department.objects.get(pk=department_id)
        template = 'IC/change_object.html'
        context = {
            'url_name': 'change_department',
            'title': 'Редактирование отдела/группы',
        }
    if request.method == 'POST':
        form = DepartmentForm(request.POST, request.FILES, instance=department)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DepartmentForm(instance=department)
        context['form'] = form
    return render(request, template, context)


class IndicatorViewSet(ModelViewSet):
    queryset = Indicator.objects.select_related(
        'department')  # жадная загрузка, чтобы по сто раз не спрашивать базу данных
    # permission_classes = [IsAuthenticated]
    serializer_class = IndicatorSerializer

    @action(detail=False, methods=['get', 'post', 'put', 'delete'], name='Settlement form')
    def settlement_form(self, request, *args, **kwargs):
        page_obj = get_page_obj(self.queryset, 6, request)
        return render(request, 'IC/settlement_form.html',
                      {'page_obj': page_obj, 'list': self.queryset})

    @action(detail=False, methods=['get', 'post', 'put', 'delete'], name='Data input')
    def data_input(self, request, *args, **kwargs):
        page_obj = get_page_obj(self.queryset, 6, request)
        return render(request, 'IC/data_input.html', {'page_obj': page_obj, 'list': self.queryset})


def forms_indicator(request, indicator_id=None):
    if indicator_id is None:
        indicator = None
        template = 'IC/add_object.html'
        context = {
            'url_name': 'add_indicator',
            'title': 'Добавление показателя',
        }
    else:
        indicator = Indicator.objects.get(pk=indicator_id)
        template = 'IC/change_object.html'
        context = {
            'url_name': 'change_indicator',
            'title': 'Редактирование показателя',
        }
    if request.method == 'POST':
        form = IndicatorForm(request.POST, request.FILES, instance=indicator)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IndicatorForm(instance=indicator)
        context['form'] = form
    return render(request, template, context)


class Critical_serviceViewSet(ModelViewSet):
    queryset = Critical_service.objects.all()
    serializer_class = Critical_serviceSerializer
    permission_classes = [IsAuthenticated]


def forms_crirtical_service(request, critical_service_id=None):
    if critical_service_id is None:
        cs = None
        template = 'IC/add_object.html'
        context = {
            'url_name': 'add_critical_service',
            'title': 'Добавление критически важного сервиса/службы',
        }
    else:
        cs = Critical_service.objects.get(pk=critical_service_id)
        template = 'IC/change_object.html'
        context = {
            'url_name': 'change_critical_service',
            'title': 'Редактирование критически важного сервиса/службы',
        }
    if request.method == 'POST':
        form = Crtitical_serviceForm(request.POST, request.FILES, instance=cs)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = Crtitical_serviceForm(instance=cs)
        context['form'] = form
    return render(request, template, context)


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'IC/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'IC/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def get_page_obj(queryset, num_objects, request=None):
    paginator = Paginator(queryset, num_objects)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


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
