from django import template
from IC.models import *
from IC.views import *
register = template.Library()

@register.simple_tag(name='some_function')
def your_function():
    return True

@register.inclusion_tag('IC/critical_services.html')
def show_critical_service(request):
    critical_services = Critical_service.objects.all()
    page_obj = get_page_obj(Critical_service.objects.all(), request, 1)
    return {"page_obj": page_obj, "critical_services": critical_services}

@register.inclusion_tag('IC/pagination.html')
def show_pagination(page_obj):
    return {"page_obj": page_obj}

@register.simple_tag
def get_number(page_obj, curr_num):
    page_number = (page_obj.number - 1)*(len(page_obj.paginator.object_list)-1) + curr_num
    return (page_number)