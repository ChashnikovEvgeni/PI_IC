from django.urls import path
from rest_framework.routers import SimpleRouter
from django.conf.urls.static import static

from Accounting_table import settings
from .views import *

router = SimpleRouter()  # это djangorestframework

router.register(r'Department', DepartmentViewSet)
router.register(r'Service', ServiceViewSet)
router.register(r'Indicator', IndicatorViewSet)
router.register(r'Critical_service', Critical_serviceViewSet)
router.register(r'Indicators_file', Indicators_fileViewSet)

urlpatterns = [
    path('', index, name='home'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('Indicator/add_indicator/', forms_indicator, name='add_indicator'),
    path('Indicator/change_indicator/<int:indicator_id>', forms_indicator, name='change_indicator'),
    path('Indicator/change_files/<int:indicator_id>', change_files, name='change_files'),
    path('Indicators_file/delete_file/<int:id>', delete_file, name='delete_file'),
    path('Critical_service/add_critical_service', forms_crirtical_service, name='add_critical_service'),
    path('Critical_service/change_critical_service/<int:critical_service_id>', forms_crirtical_service, name='change_critical_service'),
    path('Department/add_department/', forms_department, name='add_department'),
    path('Department/change_department/<int:department_id>', forms_department, name='change_department'),
    path('Service/add_service/', forms_service, name='add_service'),
    path('Service/change_service/<int:service_id>', forms_service, name='change_service'),

    path('Indicator/input', data_input, name='input1'),
    path('Indicator/input/<int:indicator_id>', data_input, name='input2'),
]

urlpatterns += router.urls

print(urlpatterns)