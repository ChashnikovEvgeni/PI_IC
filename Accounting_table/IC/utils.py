

from django.db.models import Count

from .models import *

menu = [{'title': "Главная страница", 'url_name': 'home'},
        {'title': "Ввод данных за отчётный период", 'url_name': 'indicator-data-input'},
        {'title': "Отчёт отделов", 'url_name': 'department-report-departments'},
        {'title': "Расчётная форма", 'url_name': 'indicator-settlement-form'},
]

class DataMixin:
    paginate_by = 2

    def get_user_context(self, **kwargs):
        print(kwargs)
        context = kwargs
        user_menu = menu.copy()
        if self.request.user.is_authenticated:
                print('ну кек')


        context['user_menu'] = user_menu
        return context
