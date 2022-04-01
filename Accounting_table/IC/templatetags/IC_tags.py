import django.http
import requests
import rest_framework.request
from django import template
from django.http import HttpRequest

from IC.models import *
from IC.views import *
import math
register = template.Library()

@register.simple_tag(name='some_function')
def your_function():
    return True

@register.inclusion_tag('IC/critical_services.html')
def show_critical_service(request):
    print(request)
    critical_services = Critical_service.objects.all()
    page_obj = get_page_obj(Critical_service.objects.all(), 1, request)
    return {"page_obj": page_obj, "critical_services": critical_services}

@register.inclusion_tag('IC/pagination.html')
def show_pagination(page_obj):
    return {"page_obj": page_obj}

@register.simple_tag
def get_number(page_obj, curr_num):
   # page_number = (page_obj.number-1)*math.ceil(page_obj.paginator.count/page_obj.paginator.num_pages) + curr_num
    page_number = (page_obj.number-1)*(len(page_obj)+1)+curr_num
    return (page_number)