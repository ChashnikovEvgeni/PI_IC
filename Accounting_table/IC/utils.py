

from django.db.models import Count

from .models import *

from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator

#получение ограниченного списка объектов из общей их массы для вывода на экран с пагинацией
def get_page_obj(queryset, num_objects, request=None):
    paginator = Paginator(queryset, num_objects)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

