from django import template
from IC.models import *

register = template.Library()

@register.simple_tag(name='some_function')
def your_function():
    return True

@register.inclusion_tag('IC/critical_services.html')
def show_critical_service():
    critical_services = Critical_service.objects.all()
    return {"critical_services": critical_services}

